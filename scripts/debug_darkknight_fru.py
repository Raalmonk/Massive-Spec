#!/usr/bin/env python
"""Debug Futures Rewritten Dark Knight rankings and write the frontend JSON."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any
from typing import Optional

import dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

BOSS_SLUG = "futures-rewritten"
SPEC_SLUG = "darkknight-darkknight"
DIFFICULTY = "ultimate"
METRIC = "rdps"
LIMIT = 3

dotenv.load_dotenv(PROJECT_ROOT / ".env")

if not os.getenv("WCL_AUTH_TOKEN") and not (os.getenv("WCL_CLIENT_ID") and os.getenv("WCL_CLIENT_SECRET")):
    raise RuntimeError(
        "Missing FF Logs credentials. Set WCL_AUTH_TOKEN, or set both WCL_CLIENT_ID and WCL_CLIENT_SECRET."
    )

os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

from lorgs import data  # noqa: E402,F401  # load static data registrations
from lorgs.clients.wcl.client import WarcraftlogsClient  # noqa: E402
from lorgs.models.raid_boss import RaidBoss  # noqa: E402
from lorgs.models.raid_zone import RaidZone  # noqa: E402
from lorgs.models.warcraftlogs_ranking import SpecRanking  # noqa: E402
from lorgs.models.wow_spec import WowSpec  # noqa: E402


def resolve_zone_id(boss: RaidBoss) -> Optional[int]:
    for zone in RaidZone.list():
        if boss in zone.bosses:
            return zone.id
    return None


def count_fight_casts(fight: Any) -> int:
    boss_casts = len(fight.boss.casts) if fight.boss else 0
    return boss_casts + sum(len(player.casts) for player in fight.players)


async def debug_darkknight_fru() -> None:
    boss = RaidBoss.get(full_name_slug=BOSS_SLUG)
    if not boss:
        raise ValueError(f"Boss not found: {BOSS_SLUG}")

    spec = WowSpec.get(full_name_slug=SPEC_SLUG)
    if not spec:
        raise ValueError(f"Spec not found: {SPEC_SLUG}")

    ranking = SpecRanking(
        boss_slug=BOSS_SLUG,
        spec_slug=SPEC_SLUG,
        difficulty=DIFFICULTY,
        metric=METRIC,
    )
    await ranking.load(limit=LIMIT, clear_old=True)

    output_path = PROJECT_ROOT / "front_end" / "data" / f"spec_ranking_{SPEC_SLUG}_{BOSS_SLUG}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(ranking.model_dump(exclude_unset=True, by_alias=True), ensure_ascii=False, default=str),
        encoding="utf-8",
    )

    cast_counts = [count_fight_casts(fight) for fight in ranking.fights]
    phase_counts = [len(fight.phases) for fight in ranking.fights]
    zone_id = resolve_zone_id(boss)

    print("Futures Rewritten Dark Knight debug complete")
    print(f"boss slug: {boss.full_name_slug}")
    print(f"boss id: {boss.id}")
    print(f"zone id: {zone_id if zone_id is not None else 'unknown'}")
    print(f"spec slug: {spec.full_name_slug}")
    print(f"difficulty: {DIFFICULTY}")
    print(f"metric: {METRIC}")
    print(f"fights loaded: {len(ranking.fights)}")
    print(f"casts per fight: {cast_counts}")
    print(f"phases per fight: {phase_counts}")
    print(f"output path: {output_path}")

    if not any(phase_counts):
        print("No native FF Logs phases found for these fights.")


async def main() -> None:
    try:
        await debug_darkknight_fru()
    finally:
        client = WarcraftlogsClient._instance
        if client and client.session:
            await client.session.close()
            await asyncio.sleep(0.25)


if __name__ == "__main__":
    asyncio.run(main())
