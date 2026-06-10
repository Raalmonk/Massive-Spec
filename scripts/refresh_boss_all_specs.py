#!/usr/bin/env python
"""Force refresh one boss for every spec and write frontend JSON."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

import aiohttp
import dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_LIMIT = 100
DELAY_SECONDS = 1.0

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
from lorgs.data.classes import ALL_SPECS  # noqa: E402
from lorgs.models.raid_boss import RaidBoss  # noqa: E402
from lorgs.models.warcraftlogs_ranking import SpecRanking  # noqa: E402
from updater import BOSS_CONFIG, DEFAULT_METRIC, DEFAULT_RANKING_REGIONS  # noqa: E402


def parse_ranking_regions(raw_regions: list[str]) -> tuple[str, ...]:
    regions = []
    for raw_region in raw_regions:
        region = raw_region.strip()
        if region.lower() in ("global", "gl", "www", "intl", "international"):
            region = ""
        elif region.lower() == "cn":
            region = "CN"
        elif region.lower() in ("kr", "ko", "korea", "korean"):
            region = "KR"
        elif region:
            region = region.upper()
        regions.append(region)

    return tuple(dict.fromkeys(regions))


def count_regions(ranking: SpecRanking) -> dict[str, int]:
    counts = {"global": 0, "cn": 0, "kr": 0}
    for report in ranking.reports:
        region = (report.region or "").upper()
        if region == "CN":
            counts["cn"] += len(report.fights)
        elif region == "KR":
            counts["kr"] += len(report.fights)
        else:
            counts["global"] += len(report.fights)
    return counts


def get_boss_config(boss_slug: str) -> tuple[str, str, tuple[str, ...]]:
    config = BOSS_CONFIG.get(boss_slug, {})
    difficulty = config.get("difficulty", "mythic")
    metric = config.get("metric", DEFAULT_METRIC)
    ranking_regions = tuple(config.get("ranking_regions", DEFAULT_RANKING_REGIONS))
    return difficulty, metric, ranking_regions


async def refresh_spec(
    boss_slug: str,
    spec,
    difficulty: str,
    metric: str,
    limit: int,
    ranking_regions: tuple[str, ...],
) -> tuple[str, int, dict[str, int], Path | None, str]:
    spec_slug = spec.full_name_slug
    ranking = SpecRanking(
        boss_slug=boss_slug,
        spec_slug=spec_slug,
        difficulty=difficulty,
        metric=metric,
    )

    await ranking.load(limit=limit, clear_old=True, ranking_regions=ranking_regions)
    fight_count = len(ranking.fights)
    region_counts = count_regions(ranking)

    if not fight_count:
        return spec_slug, 0, region_counts, None, "no fights"

    output_path = PROJECT_ROOT / "front_end" / "data" / f"spec_ranking_{spec_slug}_{boss_slug}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(ranking.model_dump(exclude_unset=True, by_alias=True), ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    return spec_slug, fight_count, region_counts, output_path, "written"


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--boss", required=True, help="Boss slug, for example the-tyrant.")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--metric", help="Override the metric from updater.py.")
    parser.add_argument("--difficulty", help="Override the difficulty from updater.py.")
    parser.add_argument("--delay", type=float, default=DELAY_SECONDS)
    parser.add_argument("--spec", action="append", help="Only refresh this spec slug. Can be passed multiple times.")
    parser.add_argument(
        "--regions",
        nargs="+",
        help="Ranking endpoints to query. Defaults to updater.py boss config, usually global cn kr.",
    )
    args = parser.parse_args()

    if not RaidBoss.get(full_name_slug=args.boss):
        raise RuntimeError(f"Unknown boss slug: {args.boss}")

    config_difficulty, config_metric, config_regions = get_boss_config(args.boss)
    difficulty = args.difficulty or config_difficulty
    metric = args.metric or config_metric
    ranking_regions = parse_ranking_regions(args.regions) if args.regions else config_regions

    specs = sorted(list(ALL_SPECS), key=lambda spec: spec.full_name_slug)
    if args.spec:
        requested_specs = set(args.spec)
        specs = [spec for spec in specs if spec.full_name_slug in requested_specs]
        missing_specs = sorted(requested_specs - {spec.full_name_slug for spec in specs})
        if missing_specs:
            raise RuntimeError(f"Unknown spec slug(s): {', '.join(missing_specs)}")

    written = 0
    skipped = 0
    failed = 0

    try:
        region_label = ", ".join(region or "global" for region in ranking_regions)
        print(
            f"Refreshing {args.boss} for {len(specs)} specs | "
            f"difficulty={difficulty} | metric={metric} | limit={args.limit} | regions={region_label}"
        )
        for index, spec in enumerate(specs, start=1):
            spec_slug = spec.full_name_slug
            print(f"[{index}/{len(specs)}] {spec_slug} ...", flush=True)
            try:
                spec_slug, fight_count, region_counts, output_path, status = await refresh_spec(
                    args.boss,
                    spec,
                    difficulty,
                    metric,
                    args.limit,
                    ranking_regions,
                )
            except aiohttp.ClientResponseError as error:
                failed += 1
                print(f"  failed: HTTP {error.status} {error.message}")
                continue
            except Exception as error:
                failed += 1
                print(f"  failed: {error}")
                continue

            if fight_count:
                written += 1
                print(
                    "  written: "
                    f"fights={fight_count} "
                    f"global={region_counts['global']} "
                    f"cn={region_counts['cn']} "
                    f"kr={region_counts['kr']} "
                    f"path={output_path}"
                )
            else:
                skipped += 1
                print(f"  skipped: {status}")

            if args.delay > 0:
                await asyncio.sleep(args.delay)

        print(f"{args.boss} all-spec refresh complete")
        print(f"written specs: {written}")
        print(f"skipped specs: {skipped}")
        print(f"failed specs: {failed}")
    finally:
        client = WarcraftlogsClient._instance
        if client and client.session:
            await client.session.close()
            await asyncio.sleep(0.25)


if __name__ == "__main__":
    asyncio.run(main())
