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
from lorgs.data.expansions.dawntrail import raids  # Load FFXIV Raids
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

    # Force DPS for Healers
    if spec.role.code == "heal":
        metric = "dps"

    # 2. Query Rankings
    client = wcl.WarcraftlogsClient.get_instance()

    difficulty_id = 5 # Mythic
    if difficulty == "heroic": difficulty_id = 4
    elif difficulty == "normal": difficulty_id = 3

    def build_rankings_query(args=""):
        # Viper (Class==Spec) Fix:
        spec_name_arg = f'specName: "{spec.name_slug_cap}"'
        if spec.wow_class.name_slug_cap == spec.name_slug_cap:
             spec_name_arg = ""

        return f"""
            characterRankings(
                className: "{spec.wow_class.name_slug_cap}"
                {spec_name_arg}
                metric: {metric}
                difficulty: {difficulty_id}
                includeCombatantInfo: true
                page: 1
                {args}
            )
        """

    query = f"""
    worldData
    {{
        encounter(id: {boss.id})
        {{
            {build_rankings_query()}
            cn: {build_rankings_query('serverRegion: "CN"')}
        }}
    }}
    """

    logger.info(f"Fetching top {limit} ranks for {boss.name} - {spec.name}...")
    result = await client.query(query)
    encounter_data = result.get("worldData", {}).get("encounter", {})

    global_rankings = encounter_data.get("characterRankings", {}).get("rankings", [])
    cn_rankings = encounter_data.get("cn", {}).get("rankings", [])

    logger.info(f"CN Rankings found: {len(cn_rankings)}")

    # Merge: Global (limit) + CN (10)
    rankings = global_rankings[:limit] + cn_rankings[:10]

    # Sort by DPS
    rankings.sort(key=lambda x: x.get("amount", 0), reverse=True)

    for i, rank in enumerate(rankings):
        report_id = rank.get("report", {}).get("code")
        fight_id = rank.get("report", {}).get("fightID")
        player_name = rank.get("name")
        amount = rank.get("amount") # Player DPS

        logger.info(f"[{i+1}/{limit}] Checking Report: {report_id} Fight: {fight_id} ({player_name})")

        # Partners
        partners = []
        if spec.role.code in ("tank", "heal") and rank.get("combatantInfo"):
            for c in rank.get("combatantInfo"):
                c_name = c.get("name")
                if c_name == player_name: continue

                # Resolve Spec/Role
                c_spec_name = c.get("spec") or c.get("type") # Handle Jobs with no spec
                c_spec = WowSpec.get(name_slug_cap=c_spec_name)
                if not c_spec: c_spec = WowSpec.get(name_slug_cap=c.get("type"))

                if c_spec and c_spec.role == spec.role:
                    partners.append(f"{c_name} ({c_spec.name})")

        if partners:
            logger.info(f"   -> Partner(s): {', '.join(partners)}")

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
