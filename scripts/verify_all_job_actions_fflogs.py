#!/usr/bin/env python
"""Verify generated FF14 job action IDs against FF Logs game data."""

from __future__ import annotations

import argparse
import asyncio
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

import dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

dotenv.load_dotenv(PROJECT_ROOT / ".env")

os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")

from lorgs.clients.wcl.client import WarcraftlogsClient  # noqa: E402
from lorgs.data.classes.all_actions import ALL_ACTIONS_BY_SPEC  # noqa: E402


def normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip()).casefold()


def chunked(values: list[int], size: int) -> list[list[int]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


async def query_abilities(ids: list[int], chunk_size: int) -> dict[int, dict]:
    client = WarcraftlogsClient.get_instance()
    abilities: dict[int, dict] = {}

    for chunk in chunked(ids, chunk_size):
        fields = "\n".join(
            f'a{ability_id}: ability(id: {ability_id}) {{ id name }}'
            for ability_id in chunk
        )
        result = await client.query(f"gameData {{ {fields} }}", raise_errors=False)
        game_data = result.get("gameData") or {}
        for ability_id in chunk:
            abilities[ability_id] = game_data.get(f"a{ability_id}") or {}

    return abilities


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunk-size", type=int, default=80)
    args = parser.parse_args()

    expected_by_id: dict[int, set[str]] = defaultdict(set)
    specs_by_id: dict[int, set[str]] = defaultdict(set)
    duplicate_rows = 0

    for spec_slug, actions in ALL_ACTIONS_BY_SPEC.items():
        seen_for_spec: set[int] = set()
        for action in actions:
            ability_id = int(action["spell_id"])
            expected_by_id[ability_id].add(action["name"])
            specs_by_id[ability_id].add(spec_slug)
            if ability_id in seen_for_spec:
                duplicate_rows += 1
            seen_for_spec.add(ability_id)

    ids = sorted(expected_by_id)
    abilities = await query_abilities(ids, args.chunk_size)

    missing: list[tuple[int, list[str], list[str]]] = []
    mismatched: list[tuple[int, list[str], str, list[str]]] = []
    matched = 0

    for ability_id in ids:
        expected_names = sorted(expected_by_id[ability_id])
        specs = sorted(specs_by_id[ability_id])
        actual_name = (abilities.get(ability_id) or {}).get("name") or ""

        if not actual_name:
            missing.append((ability_id, expected_names, specs))
            continue

        normalized_actual = normalize_name(actual_name)
        if normalized_actual not in {normalize_name(name) for name in expected_names}:
            mismatched.append((ability_id, expected_names, actual_name, specs))
            continue

        matched += 1

    print("FF Logs ability verification complete")
    print(f"specs: {len(ALL_ACTIONS_BY_SPEC)}")
    print(f"action rows: {sum(len(actions) for actions in ALL_ACTIONS_BY_SPEC.values())}")
    print(f"unique ability ids: {len(ids)}")
    print(f"matched ids: {matched}")
    print(f"missing ids: {len(missing)}")
    print(f"name mismatches: {len(mismatched)}")
    print(f"duplicate rows within one spec: {duplicate_rows}")

    if missing:
        print("\nMissing IDs:")
        for ability_id, expected_names, specs in missing[:50]:
            print(f"  {ability_id}: {expected_names} specs={specs}")
        if len(missing) > 50:
            print(f"  ... {len(missing) - 50} more")

    if mismatched:
        print("\nName mismatches:")
        for ability_id, expected_names, actual_name, specs in mismatched[:80]:
            print(f"  {ability_id}: expected={expected_names} actual={actual_name!r} specs={specs}")
        if len(mismatched) > 80:
            print(f"  ... {len(mismatched) - 80} more")

    if missing or mismatched:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        client = WarcraftlogsClient._instance
        if client and client.session and not client.session.closed:
            asyncio.run(client.session.close())
