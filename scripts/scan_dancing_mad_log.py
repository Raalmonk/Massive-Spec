#!/usr/bin/env python
"""Scan one Dancing Mad FF Logs pull into local frontend ranking JSON files."""

from __future__ import annotations

import argparse
import asyncio
import copy
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs
from urllib.parse import urlparse

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
DEFAULT_URL = "https://www.fflogs.com/reports/FvV3yLNQbJGaDdBh?fight=last&type=summary"

dotenv.load_dotenv(PROJECT_ROOT / ".env")

if not os.getenv("WCL_AUTH_TOKEN") and not (os.getenv("WCL_CLIENT_ID") and os.getenv("WCL_CLIENT_SECRET")):
    raise RuntimeError(
        "Missing FF Logs credentials. Set WCL_AUTH_TOKEN, or set both WCL_CLIENT_ID and WCL_CLIENT_SECRET."
    )

os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")

from lorgs import data  # noqa: E402,F401  # load static data registrations
from lorgs.clients.wcl.client import WarcraftlogsClient  # noqa: E402
from lorgs.models.raid_boss import RaidBoss  # noqa: E402
from lorgs.models.warcraftlogs_report import Report  # noqa: E402
from lorgs.models.warcraftlogs_ranking import SpecRanking  # noqa: E402
from lorgs.models.wow_spec import WowSpec  # noqa: E402


def parse_report_url(url: str) -> tuple[str, str]:
    parsed = urlparse(url.strip())
    match = re.search(r"/reports/([A-Za-z0-9]+)", parsed.path)
    report_id = match.group(1) if match else ""
    fight_raw = (parse_qs(parsed.query).get("fight") or ["last"])[0]

    if not report_id:
        raise ValueError("Could not find report id in URL.")

    return report_id, fight_raw


def select_fight(report: Report, fight_raw: str, boss_slug: str):
    if fight_raw.isdigit():
        fight = report.get_fight(fight_id=int(fight_raw))
        if not fight:
            raise ValueError(f"Fight not found: {fight_raw}")
        return fight

    if fight_raw != "last":
        raise ValueError(f"Unsupported fight selector: {fight_raw}. Use a number or 'last'.")

    boss = RaidBoss.get(full_name_slug=boss_slug)
    boss_fights = [
        fight
        for fight in report.fights
        if fight.boss and fight.boss.raid_boss and boss and fight.boss.raid_boss.id == boss.id
    ]
    fights = boss_fights or [fight for fight in report.fights if fight.boss]
    if not fights:
        raise ValueError("No boss fights found in report.")

    return fights[-1]


def ranking_path(spec_slug: str) -> Path:
    return PROJECT_ROOT / "front_end" / "data" / f"spec_ranking_{spec_slug}_{BOSS_SLUG}.json"


def empty_ranking_payload(spec_slug: str, metric: str) -> dict:
    return {
        "spec_slug": spec_slug,
        "boss_slug": BOSS_SLUG,
        "difficulty": DIFFICULTY,
        "metric": metric,
        "reports": [],
    }


def load_ranking_payload(spec_slug: str, metric: str) -> dict:
    path = ranking_path(spec_slug)
    if not path.exists():
        return empty_ranking_payload(spec_slug, metric)

    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.setdefault("spec_slug", spec_slug)
    payload.setdefault("boss_slug", BOSS_SLUG)
    payload.setdefault("difficulty", DIFFICULTY)
    payload.setdefault("metric", metric)
    payload.setdefault("reports", [])
    return payload


def upsert_fight(payload: dict, report_payload: dict, fight_id: int) -> None:
    report_id = report_payload["report_id"]
    reports = []

    for existing_report in payload.get("reports", []):
        if existing_report.get("report_id") != report_id:
            reports.append(existing_report)
            continue

        fights = [
            fight
            for fight in existing_report.get("fights", [])
            if int(fight.get("fight_id", -1)) != fight_id
        ]
        if fights:
            existing_report["fights"] = fights
            reports.append(existing_report)

    reports.append(copy.deepcopy(report_payload))
    payload["reports"] = reports


async def load_metric_totals(report_id: str, fight_id: int, metric: str) -> dict[tuple[str, str], float]:
    query = f"""
        reportData
        {{
            report(code: "{report_id}")
            {{
                rankings(fightIDs: [{fight_id}], playerMetric: {metric})
            }}
        }}
    """
    result = await WarcraftlogsClient.get_instance().query(query, raise_errors=False)
    rankings_payload = (
        result.get("reportData", {})
        .get("report", {})
        .get("rankings", {})
    )

    totals: dict[tuple[str, str], float] = {}
    for _fight_id, name, spec_slug, amount in SpecRanking._iter_report_ranking_characters(rankings_payload):
        if int(_fight_id) != int(fight_id):
            continue
        totals[(SpecRanking._normalize_name(name), spec_slug)] = float(amount)
    return totals


def apply_metric_totals(fight, totals: dict[tuple[str, str], float]) -> int:
    applied = 0
    for player in fight.players:
        total = totals.get((SpecRanking._normalize_name(player.name), player.spec_slug))
        if total is None:
            continue
        if abs(player.total - total) > 0.1:
            player.total = total
            applied += 1
    return applied


async def scan_log(url: str, metric: str, boss_slug: str, dry_run: bool) -> None:
    report_id, fight_raw = parse_report_url(url)
    report = Report(report_id=report_id)

    print(f"Loading report {report_id} fight={fight_raw} metric={metric}")
    await report.load(raise_errors=True)
    fight = select_fight(report, fight_raw, boss_slug)

    print(f"Selected fight: id={fight.fight_id} boss={fight.boss_slug if hasattr(fight, 'boss_slug') else boss_slug}")
    await fight.load(raise_errors=True)

    totals = await load_metric_totals(report.report_id, fight.fight_id, metric)
    applied = apply_metric_totals(fight, totals)
    print(f"Applied {metric.upper()} totals: {applied}/{len(fight.players)} players")

    print("Loading casts for all players and boss...")
    await fight.load_actors()
    applied_after_casts = apply_metric_totals(fight, totals)
    if applied_after_casts:
        print(f"Re-applied {metric.upper()} totals after cast load: {applied_after_casts}/{len(fight.players)} players")

    report_payload = report.model_dump(exclude_unset=True, by_alias=True)
    report_payload["fights"] = [fight.model_dump(exclude_unset=True, by_alias=True)]
    report_payload["region"] = report.region or report_payload.get("region", "")

    spec_slugs = sorted({player.spec_slug for player in fight.players if player.spec_slug and WowSpec.get(full_name_slug=player.spec_slug)})
    if not spec_slugs:
        raise RuntimeError("No registered specs found in selected fight.")

    written = []
    for spec_slug in spec_slugs:
        payload = load_ranking_payload(spec_slug, metric)
        payload["metric"] = metric
        upsert_fight(payload, report_payload, fight.fight_id)

        if dry_run:
            continue

        path = ranking_path(spec_slug)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, default=str), encoding="utf-8")
        written.append(path)

    print("Players:")
    for player in sorted(fight.players, key=lambda p: (p.spec_slug, p.name)):
        print(
            f"  {player.source_id:>3} {player.spec_slug:<32} "
            f"{player.total:>10.1f} casts={len(player.casts):>3} {player.name}"
        )

    print(f"Specs touched: {len(spec_slugs)}")
    for spec_slug in spec_slugs:
        print(f"  {spec_slug}")

    if dry_run:
        print("Dry run complete; no files written.")
    else:
        print(f"Wrote {len(written)} frontend ranking files.")
        for path in written:
            print(f"  {path}")


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs="?", default=DEFAULT_URL)
    parser.add_argument("--metric", default=DEFAULT_METRIC, choices=[DEFAULT_METRIC])
    parser.add_argument("--boss", default=BOSS_SLUG)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        await scan_log(url=args.url, metric=args.metric, boss_slug=args.boss, dry_run=args.dry_run)
    finally:
        client = WarcraftlogsClient._instance
        if client and client.session:
            await client.session.close()
            await asyncio.sleep(0.25)


if __name__ == "__main__":
    asyncio.run(main())
