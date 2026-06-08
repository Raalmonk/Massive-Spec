#!/usr/bin/env python
"""Force refresh Dancing Mad rankings for every spec and write frontend JSON."""

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

BOSS_SLUG = "dancing-mad"
DIFFICULTY = "ultimate"
DEFAULT_METRIC = "rdps"
DEFAULT_LIMIT = 100
DELAY_SECONDS = 1.0
DEFAULT_RANKING_REGIONS = ("", "CN", "KR")

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
from lorgs.models.warcraftlogs_ranking import SpecRanking  # noqa: E402


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


async def refresh_spec(
    spec,
    limit: int,
    metric: str,
    ranking_regions: tuple[str, ...],
) -> tuple[str, int, dict[str, int], Path | None, str]:
    spec_slug = spec.full_name_slug
    ranking = SpecRanking(
        boss_slug=BOSS_SLUG,
        spec_slug=spec_slug,
        difficulty=DIFFICULTY,
        metric=metric,
    )

    await ranking.load(limit=limit, clear_old=True, ranking_regions=ranking_regions)
    fight_count = len(ranking.fights)
    region_counts = count_regions(ranking)

    if not fight_count:
        return spec_slug, 0, region_counts, None, "no fights"

    output_path = PROJECT_ROOT / "front_end" / "data" / f"spec_ranking_{spec_slug}_{BOSS_SLUG}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(ranking.model_dump(exclude_unset=True, by_alias=True), ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    return spec_slug, fight_count, region_counts, output_path, "written"


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--metric", default=DEFAULT_METRIC, choices=[DEFAULT_METRIC])
    parser.add_argument("--delay", type=float, default=DELAY_SECONDS)
    parser.add_argument("--spec", action="append", help="Only refresh this spec slug. Can be passed multiple times.")
    parser.add_argument(
        "--regions",
        nargs="+",
        default=[region or "global" for region in DEFAULT_RANKING_REGIONS],
        help="Ranking endpoints to query. Defaults to global cn kr.",
    )
    args = parser.parse_args()

    ranking_regions = parse_ranking_regions(args.regions)
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
            f"Refreshing Dancing Mad for {len(specs)} specs | "
            f"metric={args.metric} | limit={args.limit} | regions={region_label}"
        )
        for index, spec in enumerate(specs, start=1):
            spec_slug = spec.full_name_slug
            print(f"[{index}/{len(specs)}] {spec_slug} ...", flush=True)
            try:
                spec_slug, fight_count, region_counts, output_path, status = await refresh_spec(
                    spec,
                    args.limit,
                    args.metric,
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

        print("Dancing Mad all-spec refresh complete")
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
