#!/usr/bin/env python
"""Fetch Top Ranks for a given Boss and Spec, with Smart Caching."""

# IMPORT STANDARD LIBRARIES
import argparse
import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

# Mock AWS credentials to prevent boto3 initialization errors if not set
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")

import dotenv
dotenv.load_dotenv()

# IMPORT LOCAL LIBRARIES
from lorgs import data  # load static data
from lorgs.clients import wcl
from lorgs.models.warcraftlogs_user_report import UserReport
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.wow_spec import WowSpec
from lorgs.logger import logger

async def fetch_top_ranks(boss_slug, spec_slug, limit=5, difficulty="mythic", metric="dps"):
    # 1. Resolve IDs
    boss = RaidBoss.get(full_name_slug=boss_slug)
    if not boss:
        logger.error(f"Boss not found: {boss_slug}")
        return

    spec = WowSpec.get(full_name_slug=spec_slug)
    if not spec:
        logger.error(f"Spec not found: {spec_slug}")
        return

    # Force Metric for Healers
    if spec.role.code == "heal":
        metric = "dps"

    # 2. Query Rankings
    client = wcl.WarcraftlogsClient.get_instance()

    difficulty_id = 5 # Mythic
    if difficulty == "heroic": difficulty_id = 4
    elif difficulty == "normal": difficulty_id = 3

    def build_query(region=None):
        region_arg = f'serverRegion: "{region}"' if region else ""
        return f"""
        worldData
        {{
            encounter(id: {boss.id})
            {{
                characterRankings(
                    className: "{spec.wow_class.name_slug_cap}"
                    specName: "{spec.name_slug_cap}"
                    metric: {metric}
                    difficulty: {difficulty_id}
                    includeCombatantInfo: true
                    page: 1
                    {region_arg}
                )
            }}
        }}
        """

    logger.info(f"Fetching rankings for {boss.name} - {spec.name}...")

    # Dual Fetch: Global (Top 5) + CN (Top 10)
    q_global = build_query(region="Global")
    q_cn = build_query(region="CN")

    results = await asyncio.gather(client.query(q_global), client.query(q_cn), return_exceptions=True)

    rankings = []

    # Process Global
    res_global = results[0]
    if isinstance(res_global, dict):
        r = res_global.get("worldData", {}).get("encounter", {}).get("characterRankings", {}).get("rankings", [])
        rankings.extend(r[:5])

    # Process CN
    res_cn = results[1]
    if isinstance(res_cn, dict):
        r = res_cn.get("worldData", {}).get("encounter", {}).get("characterRankings", {}).get("rankings", [])
        rankings.extend(r[:10])

    for i, rank in enumerate(rankings):
        report_id = rank.get("report", {}).get("code")
        fight_id = rank.get("report", {}).get("fightID")
        player_name = rank.get("name")
        amount = rank.get("amount") # Player DPS

        # Extract party composition
        combatant_info = []
        # Assumption: combatantInfo is a list of objects with 'spec' or 'icon' that we can map to slugs
        # WCL API v2: combatantInfo is not always documented clearly for this endpoint,
        # but let's try to extract it if present.
        # Based on previous knowledge, characterRankings with includeCombatantInfo: true
        # *should* have it, but sometimes it might be missing or different format.
        # Use a safe extraction.

        # Note: If combatantInfo is not directly usable to match exactly, we rely on report_id+fight_id
        # and checking if the cached fight has *any* combatant info.

        # Let's inspect the rank object for debug if needed, but here we just proceed.

        logger.info(f"[{i+1}/{limit}] Checking Report: {report_id} Fight: {fight_id} ({player_name})")

        # Check Cache
        try:
            report = UserReport.get(report_id=report_id)
        except Exception:
            report = None

        existing_fight = None
        if report:
             existing_fight = report.get_fight(fight_id)

        if existing_fight:
             # Verify Cache
             # 1. Must be fully loaded (damage_done > 0)
             # 2. Must have combatant_info populated

             if existing_fight.combatant_info and existing_fight.damage_done > 0:
                 # Optional: Deeper verification could go here.
                 # e.g. check if player_name is in the fight and has matching DPS

                 logger.info(f"   -> Skipping (Already Cached)")
                 continue

        # Load
        logger.info(f"   -> MISS. Loading...")
        user_report = UserReport(report_id=report_id)

        # We load the master data first
        await user_report.load()

        # Load the specific fight
        await user_report.load_fights(fight_ids=[fight_id], player_ids=[])

        # Post-Load Verification/Update
        fight = user_report.get_fight(fight_id)
        if fight:
            # combatant_info and damage_done should have been populated by process_players
            logger.info(f"   -> Loaded Fight. Raid DPS: {fight.damage_done}")
            logger.info(f"   -> Party: {fight.combatant_info}")

            # Save to DB
            user_report.save()
            logger.info("   -> Saved.")
        else:
            logger.warning("   -> Failed to load fight object after fetch.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--boss", type=str, required=True, help="Boss Slug (e.g. vamp-fatale)")
    parser.add_argument("--spec", type=str, default="red-mage-red-mage", help="Spec Slug (e.g. red-mage-red-mage)")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--difficulty", type=str, default="mythic")
    args = parser.parse_args()

    asyncio.run(fetch_top_ranks(args.boss, args.spec, args.limit, args.difficulty))
