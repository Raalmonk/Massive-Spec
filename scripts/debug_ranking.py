#!/usr/bin/env python
"""Debug one FFLogs boss/spec ranking and write the frontend JSON."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

import dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")
dotenv.load_dotenv(PROJECT_ROOT / ".env")

from lorgs import data  # noqa: F401  # load static data registrations
from lorgs.clients.wcl.client import WarcraftlogsClient
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import RaidZone
from lorgs.models.warcraftlogs_ranking import SpecRanking
from lorgs.models.wow_spec import WowSpec


def resolve_zone_id(boss: RaidBoss) -> int:
    for zone in RaidZone.list():
        if boss in zone.bosses:
            return zone.id
    return 0


def count_fight_casts(fight: Any) -> int:
    boss_casts = len(fight.boss.casts) if fight.boss else 0
    return boss_casts + sum(len(player.casts) for player in fight.players)


async def debug_ranking(
    boss_slug: str,
    spec_slug: str,
    difficulty: str,
    metric: str,
    limit: int,
    clear: bool,
) -> None:
    boss = RaidBoss.get(full_name_slug=boss_slug)
    if not boss:
        raise ValueError(f"Boss not found: {boss_slug}")

    spec = WowSpec.get(full_name_slug=spec_slug)
    if not spec:
        raise ValueError(f"Spec not found: {spec_slug}")

    ranking = SpecRanking.get_or_create(
        boss_slug=boss_slug,
        spec_slug=spec_slug,
        difficulty=difficulty,
        metric=metric,
    )

    await ranking.load(limit=limit, clear_old=clear)

    output_path = PROJECT_ROOT / "front_end" / "data" / f"spec_ranking_{spec_slug}_{boss_slug}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(ranking.model_dump(exclude_unset=True, by_alias=True), ensure_ascii=False, default=str),
        encoding="utf-8",
    )

    print(f"resolved boss slug: {boss.full_name_slug}")
    print(f"resolved zone id: {resolve_zone_id(boss)}")
    print(f"resolved difficulty: {difficulty}")
    print(f"resolved metric: {metric}")
    print(f"number of fights loaded: {len(ranking.fights)}")
    for idx, fight in enumerate(ranking.fights, start=1):
        print(
            f"fight {idx}: report={fight.report.report_id if fight.report else ''} "
            f"fight_id={fight.fight_id} casts={count_fight_casts(fight)} phases={len(fight.phases)}"
        )
    print(f"output JSON path: {output_path}")


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--boss", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--difficulty", default="mythic")
    parser.add_argument("--metric", default="rdps")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--clear", action="store_true")
    args = parser.parse_args()

    try:
        await debug_ranking(
            boss_slug=args.boss,
            spec_slug=args.spec,
            difficulty=args.difficulty,
            metric=args.metric,
            limit=args.limit,
            clear=args.clear,
        )
    finally:
        client = WarcraftlogsClient._instance
        if client and client.session:
            await client.session.close()
            await asyncio.sleep(0.25)


if __name__ == "__main__":
    asyncio.run(main())
