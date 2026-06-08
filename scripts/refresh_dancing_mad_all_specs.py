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

BOSS_SLUG = "dancing-mad"
DIFFICULTY = "ultimate"
DEFAULT_METRIC = "rdps"
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
from lorgs.models.warcraftlogs_ranking import SpecRanking  # noqa: E402


async def refresh_spec(spec, limit: int, metric: str) -> tuple[str, int, Path | None, str]:
    spec_slug = spec.full_name_slug
    ranking = SpecRanking(
        boss_slug=BOSS_SLUG,
        spec_slug=spec_slug,
        difficulty=DIFFICULTY,
        metric=metric,
    )

    await ranking.load(limit=limit, clear_old=True)
    fight_count = len(ranking.fights)

    if not fight_count:
        return spec_slug, 0, None, "no fights"

    output_path = PROJECT_ROOT / "front_end" / "data" / f"spec_ranking_{spec_slug}_{BOSS_SLUG}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(ranking.model_dump(exclude_unset=True, by_alias=True), ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    return spec_slug, fight_count, output_path, "written"


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--metric", default=DEFAULT_METRIC)
    parser.add_argument("--delay", type=float, default=DELAY_SECONDS)
    args = parser.parse_args()

    specs = sorted(list(ALL_SPECS), key=lambda spec: spec.full_name_slug)
    written = 0
    skipped = 0
    failed = 0

    try:
        print(f"Refreshing Dancing Mad for {len(specs)} specs | metric={args.metric} | limit={args.limit}")
        for index, spec in enumerate(specs, start=1):
            spec_slug = spec.full_name_slug
            print(f"[{index}/{len(specs)}] {spec_slug} ...", flush=True)
            try:
                spec_slug, fight_count, output_path, status = await refresh_spec(spec, args.limit, args.metric)
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
                print(f"  written: fights={fight_count} path={output_path}")
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
