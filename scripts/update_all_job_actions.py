#!/usr/bin/env python
"""Generate optional FF14 job action monitoring data.

This script combines the official FF14 job guide action lists with the
SaintCoinach/XIVAPI Action.csv IDs. It writes a runtime data module that adds
missing actions to each registered job under SpellTag.OTHER, and downloads any
missing official action icons into the frontend spell image directory.
"""

from __future__ import annotations

import csv
import html
import io
import pprint
import re
import textwrap
from pathlib import Path
from typing import Any

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "lorgs" / "data" / "classes" / "all_actions.py"
ICON_DIR = PROJECT_ROOT / "front_end" / "images" / "spells"

ACTION_CSV_URL = "https://raw.githubusercontent.com/xivapi/ffxiv-datamining/master/csv/en/Action.csv"
JOB_GUIDE_BASE_URL = "https://na.finalfantasyxiv.com/jobguide"
USER_AGENT = "M-Spec full-action updater/1.0"

JOBS = {
    "paladin-paladin": {
        "guide": "paladin",
        "spec": "PALADIN_MAIN",
        "module": "lorgs.data.classes.paladin",
        "job_id": 19,
        "base_ids": [1],
    },
    "warrior-warrior": {
        "guide": "warrior",
        "spec": "WARRIOR_MAIN",
        "module": "lorgs.data.classes.warrior",
        "job_id": 21,
        "base_ids": [3],
    },
    "darkknight-darkknight": {
        "guide": "darkknight",
        "spec": "DARK_KNIGHT_MAIN",
        "module": "lorgs.data.classes.darkknight",
        "job_id": 32,
        "base_ids": [],
    },
    "gunbreaker-gunbreaker": {
        "guide": "gunbreaker",
        "spec": "GUNBREAKER_MAIN",
        "module": "lorgs.data.classes.gunbreaker",
        "job_id": 37,
        "base_ids": [],
    },
    "whitemage-whitemage": {
        "guide": "whitemage",
        "spec": "WHITE_MAGE_MAIN",
        "module": "lorgs.data.classes.whitemage",
        "job_id": 24,
        "base_ids": [6],
    },
    "scholar-scholar": {
        "guide": "scholar",
        "spec": "SCHOLAR_MAIN",
        "module": "lorgs.data.classes.scholar",
        "job_id": 28,
        "base_ids": [26],
    },
    "astrologian-astrologian": {
        "guide": "astrologian",
        "spec": "ASTROLOGIAN_MAIN",
        "module": "lorgs.data.classes.astrologian",
        "job_id": 33,
        "base_ids": [],
    },
    "sage-sage": {
        "guide": "sage",
        "spec": "SAGE_MAIN",
        "module": "lorgs.data.classes.sage",
        "job_id": 40,
        "base_ids": [],
    },
    "monk-monk": {
        "guide": "monk",
        "spec": "MONK_MAIN",
        "module": "lorgs.data.classes.monk",
        "job_id": 20,
        "base_ids": [2],
    },
    "dragoon-dragoon": {
        "guide": "dragoon",
        "spec": "DRAGOON_MAIN",
        "module": "lorgs.data.classes.dragoon",
        "job_id": 22,
        "base_ids": [4],
    },
    "ninja-ninja": {
        "guide": "ninja",
        "spec": "NINJA_MAIN",
        "module": "lorgs.data.classes.ninja",
        "job_id": 30,
        "base_ids": [29],
    },
    "samurai-samurai": {
        "guide": "samurai",
        "spec": "SAMURAI_MAIN",
        "module": "lorgs.data.classes.samurai",
        "job_id": 34,
        "base_ids": [],
    },
    "reaper-reaper": {
        "guide": "reaper",
        "spec": "REAPER_MAIN",
        "module": "lorgs.data.classes.reaper",
        "job_id": 39,
        "base_ids": [],
    },
    "viper-viper": {
        "guide": "viper",
        "spec": "VIPER_MAIN",
        "module": "lorgs.data.classes.viper",
        "job_id": 41,
        "base_ids": [],
    },
    "bard-bard": {
        "guide": "bard",
        "spec": "BARD_MAIN",
        "module": "lorgs.data.classes.bard",
        "job_id": 23,
        "base_ids": [5],
    },
    "machinist-machinist": {
        "guide": "machinist",
        "spec": "MACHINIST_MAIN",
        "module": "lorgs.data.classes.machinist",
        "job_id": 31,
        "base_ids": [],
    },
    "dancer-dancer": {
        "guide": "dancer",
        "spec": "DANCER_MAIN",
        "module": "lorgs.data.classes.dancer",
        "job_id": 38,
        "base_ids": [],
    },
    "blackmage-blackmage": {
        "guide": "blackmage",
        "spec": "BLACK_MAGE_MAIN",
        "module": "lorgs.data.classes.blackmage",
        "job_id": 25,
        "base_ids": [7],
    },
    "summoner-summoner": {
        "guide": "summoner",
        "spec": "SUMMONER_MAIN",
        "module": "lorgs.data.classes.summoner",
        "job_id": 27,
        "base_ids": [26],
    },
    "redmage-redmage": {
        "guide": "redmage",
        "spec": "RED_MAGE_MAIN",
        "module": "lorgs.data.classes.redmage",
        "job_id": 35,
        "base_ids": [],
    },
    "pictomancer-pictomancer": {
        "guide": "pictomancer",
        "spec": "PICTOMANCER_MAIN",
        "module": "lorgs.data.classes.pictomancer",
        "job_id": 42,
        "base_ids": [],
    },
}


def sanitize_icon_name(name: str) -> str:
    safe = name.replace("/", "_").replace("\\", "_").replace(":", "")
    safe = safe.replace('"', "").replace("?", "").replace("*", "")
    safe = re.sub(r"\s+", "_", safe.strip())
    safe = safe.strip("._")
    return f"{safe or 'Action'}.png"


def normalize_action_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip()).casefold()


DISPLAY_SLOT_ALIASES: dict[str, dict[str, str]] = {}


def add_display_slot(spec_slug: str, slot_name: str, *action_names: str) -> None:
    spec_slots = DISPLAY_SLOT_ALIASES.setdefault(spec_slug, {})
    slot = f"{spec_slug}:{normalize_action_name(slot_name)}"
    for action_name in action_names:
        spec_slots[action_name] = slot


add_display_slot("paladin-paladin", "royal-authority", "Rage of Halone", "Royal Authority")
add_display_slot("paladin-paladin", "spirits-expiacion", "Spirits Within", "Expiacion")
add_display_slot("paladin-paladin", "sheltron", "Sheltron", "Holy Sheltron")
add_display_slot("paladin-paladin", "sentinel", "Sentinel", "Guardian")
add_display_slot("paladin-paladin", "requiescat", "Requiescat", "Imperator")
add_display_slot("warrior-warrior", "inner-release", "Berserk", "Inner Release")
add_display_slot("warrior-warrior", "vengeance", "Vengeance", "Damnation")
add_display_slot("warrior-warrior", "raw-intuition", "Raw Intuition", "Bloodwhetting")
add_display_slot("warrior-warrior", "inner-beast", "Inner Beast", "Fell Cleave", "Inner Chaos")
add_display_slot("warrior-warrior", "steel-cyclone", "Steel Cyclone", "Decimate", "Chaotic Cyclone")
add_display_slot("darkknight-darkknight", "blood-weapon", "Blood Weapon", "Delirium")
add_display_slot("darkknight-darkknight", "flood", "Flood of Darkness", "Flood of Shadow")
add_display_slot("darkknight-darkknight", "edge", "Edge of Darkness", "Edge of Shadow")
add_display_slot("darkknight-darkknight", "shadow-wall", "Shadow Wall", "Shadowed Vigil")
add_display_slot("darkknight-darkknight", "bloodspiller", "Bloodspiller", "Scarlet Delirium")
add_display_slot("darkknight-darkknight", "quietus", "Quietus", "Impalement")
add_display_slot("gunbreaker-gunbreaker", "danger-zone", "Danger Zone", "Blasting Zone")
add_display_slot("gunbreaker-gunbreaker", "nebula", "Nebula", "Great Nebula")
add_display_slot("gunbreaker-gunbreaker", "heart-of-stone", "Heart of Stone", "Heart of Corundum")
add_display_slot(
    "whitemage-whitemage",
    "stone-glare",
    "Stone",
    "Stone II",
    "Stone III",
    "Stone IV",
    "Glare",
    "Glare III",
)
add_display_slot("whitemage-whitemage", "glare-iv", "Glare IV")
add_display_slot("whitemage-whitemage", "aero-dia", "Aero", "Aero II", "Dia")
add_display_slot("whitemage-whitemage", "holy", "Holy", "Holy III")
add_display_slot("whitemage-whitemage", "medica-ii", "Medica II", "Medica III")
add_display_slot("scholar-scholar", "ruin-broil", "Ruin", "Broil", "Broil II", "Broil III", "Broil IV")
add_display_slot("scholar-scholar", "bio", "Bio", "Bio II", "Biolysis")
add_display_slot("scholar-scholar", "art-of-war", "Art of War", "Art of War II")
add_display_slot("scholar-scholar", "succor", "Succor", "Concitation")
add_display_slot("scholar-scholar", "adloquium", "Adloquium", "Manifestation")
add_display_slot(
    "astrologian-astrologian",
    "malefic",
    "Malefic",
    "Malefic II",
    "Malefic III",
    "Malefic IV",
    "Fall Malefic",
)
add_display_slot("astrologian-astrologian", "combust", "Combust", "Combust II", "Combust III")
add_display_slot("astrologian-astrologian", "gravity", "Gravity", "Gravity II")
add_display_slot("astrologian-astrologian", "aspected-helios", "Aspected Helios", "Helios Conjunction")
add_display_slot("sage-sage", "dosis", "Dosis", "Dosis II", "Dosis III")
add_display_slot("sage-sage", "eukrasian-dosis", "Eukrasian Dosis", "Eukrasian Dosis II", "Eukrasian Dosis III")
add_display_slot("sage-sage", "phlegma", "Phlegma", "Phlegma II", "Phlegma III")
add_display_slot("sage-sage", "dyskrasia", "Dyskrasia", "Dyskrasia II")
add_display_slot("sage-sage", "toxikon", "Toxikon", "Toxikon II")
add_display_slot("sage-sage", "physis", "Physis", "Physis II")
add_display_slot("sage-sage", "eukrasian-prognosis", "Eukrasian Prognosis", "Eukrasian Prognosis II")
add_display_slot("monk-monk", "bootshine", "Bootshine", "Leaping Opo")
add_display_slot("monk-monk", "true-strike", "True Strike", "Rising Raptor")
add_display_slot("monk-monk", "snap-punch", "Snap Punch", "Pouncing Coeurl")
add_display_slot("monk-monk", "elixir-field", "Elixir Field", "Elixir Burst")
add_display_slot("monk-monk", "flint-strike", "Flint Strike", "Rising Phoenix")
add_display_slot("monk-monk", "tornado-kick", "Tornado Kick", "Phantom Rush")
add_display_slot(
    "monk-monk",
    "meditation",
    "Steeled Meditation",
    "Inspirited Meditation",
    "Forbidden Meditation",
    "Enlightened Meditation",
)
add_display_slot("monk-monk", "forbidden-chakra", "Steel Peak", "The Forbidden Chakra")
add_display_slot("monk-monk", "enlightenment", "Howling Fist", "Enlightenment")
add_display_slot("monk-monk", "destroyer", "Arm of the Destroyer", "Shadow of the Destroyer")
add_display_slot("monk-monk", "four-point-fury", "Rockbreaker", "Four-point Fury")
add_display_slot("dragoon-dragoon", "true-thrust", "True Thrust", "Raiden Thrust")
add_display_slot("dragoon-dragoon", "vorpal-thrust", "Vorpal Thrust", "Lance Barrage")
add_display_slot("dragoon-dragoon", "full-thrust", "Full Thrust", "Heavens' Thrust")
add_display_slot("dragoon-dragoon", "disembowel", "Disembowel", "Spiral Blow")
add_display_slot("dragoon-dragoon", "chaos-thrust", "Chaos Thrust", "Chaotic Spring")
add_display_slot("dragoon-dragoon", "jump", "Jump", "High Jump")
add_display_slot("dragoon-dragoon", "doom-spike", "Doom Spike", "Draconian Fury")
add_display_slot("ninja-ninja", "assassinate", "Assassinate", "Dream Within a Dream")
add_display_slot("ninja-ninja", "trick-attack", "Trick Attack", "Kunai's Bane")
add_display_slot("ninja-ninja", "mug", "Mug", "Dokumori")
add_display_slot("ninja-ninja", "katon", "Katon", "Goka Mekkyaku")
add_display_slot("ninja-ninja", "hyoton", "Hyoton", "Hyosho Ranryu")
add_display_slot("ninja-ninja", "hellfrog", "Hellfrog Medium", "Deathfrog Medium")
add_display_slot("ninja-ninja", "bhavacakra", "Bhavacakra", "Zesho Meppo")
add_display_slot("samurai-samurai", "hakaze", "Hakaze", "Gyofu")
add_display_slot("samurai-samurai", "fuga", "Fuga", "Fuko")
add_display_slot("samurai-samurai", "third-eye", "Third Eye", "Tengentsu")
add_display_slot("samurai-samurai", "midare", "Midare Setsugekka", "Tendo Setsugekka")
add_display_slot("samurai-samurai", "kaeshi-setsugekka", "Kaeshi: Setsugekka", "Tendo Kaeshi Setsugekka")
add_display_slot("samurai-samurai", "tenka-goken", "Tenka Goken", "Tendo Goken")
add_display_slot("samurai-samurai", "kaeshi-goken", "Kaeshi: Goken", "Tendo Kaeshi Goken")
add_display_slot("reaper-reaper", "gibbet", "Gibbet", "Executioner's Gibbet")
add_display_slot("reaper-reaper", "gallows", "Gallows", "Executioner's Gallows")
add_display_slot("reaper-reaper", "guillotine", "Guillotine", "Executioner's Guillotine")
add_display_slot("bard-bard", "heavy-shot", "Heavy Shot", "Burst Shot")
add_display_slot("bard-bard", "straight-shot", "Straight Shot", "Refulgent Arrow")
add_display_slot("bard-bard", "venomous-bite", "Venomous Bite", "Caustic Bite")
add_display_slot("bard-bard", "windbite", "Windbite", "Stormbite")
add_display_slot("bard-bard", "quick-nock", "Quick Nock", "Ladonsbite")
add_display_slot("bard-bard", "wide-volley", "Wide Volley", "Shadowbite")
add_display_slot("bard-bard", "bloodletter", "Bloodletter", "Heartbreak Shot")
add_display_slot("machinist-machinist", "split-shot", "Split Shot", "Heated Split Shot")
add_display_slot("machinist-machinist", "slug-shot", "Slug Shot", "Heated Slug Shot")
add_display_slot("machinist-machinist", "clean-shot", "Clean Shot", "Heated Clean Shot")
add_display_slot("machinist-machinist", "spread-shot", "Spread Shot", "Scattergun")
add_display_slot("machinist-machinist", "hot-shot", "Hot Shot", "Air Anchor")
add_display_slot("machinist-machinist", "heat-blast", "Heat Blast", "Blazing Shot")
add_display_slot("machinist-machinist", "gauss-round", "Gauss Round", "Double Check")
add_display_slot("machinist-machinist", "ricochet", "Ricochet", "Checkmate")
add_display_slot("machinist-machinist", "rook", "Rook Autoturret", "Automaton Queen")
add_display_slot("machinist-machinist", "rook-overdrive", "Rook Overdrive", "Queen Overdrive")
add_display_slot("blackmage-blackmage", "thunder-single", "Thunder", "Thunder III", "High Thunder")
add_display_slot("blackmage-blackmage", "thunder-aoe", "Thunder II", "Thunder IV", "High Thunder II")
add_display_slot("blackmage-blackmage", "fire-ii", "Fire II", "High Fire II")
add_display_slot("blackmage-blackmage", "blizzard-ii", "Blizzard II", "High Blizzard II")
add_display_slot("summoner-summoner", "ruin", "Ruin", "Ruin II", "Ruin III")
add_display_slot("summoner-summoner", "outburst", "Outburst", "Tri-disaster")
add_display_slot("summoner-summoner", "fester", "Fester", "Necrotize")
add_display_slot("summoner-summoner", "ruby-ruin", "Ruby Ruin", "Ruby Ruin II", "Ruby Ruin III", "Ruby Rite")
add_display_slot("summoner-summoner", "topaz-ruin", "Topaz Ruin", "Topaz Ruin II", "Topaz Ruin III", "Topaz Rite")
add_display_slot("summoner-summoner", "emerald-ruin", "Emerald Ruin", "Emerald Ruin II", "Emerald Ruin III", "Emerald Rite")
add_display_slot("summoner-summoner", "ruby-outburst", "Ruby Outburst", "Ruby Disaster", "Ruby Catastrophe")
add_display_slot("summoner-summoner", "topaz-outburst", "Topaz Outburst", "Topaz Disaster", "Topaz Catastrophe")
add_display_slot("summoner-summoner", "emerald-outburst", "Emerald Outburst", "Emerald Disaster", "Emerald Catastrophe")
add_display_slot(
    "summoner-summoner",
    "summon-bahamut",
    "Aethercharge",
    "Dreadwyrm Trance",
    "Summon Bahamut",
    "Summon Phoenix",
    "Summon Solar Bahamut",
)
add_display_slot("summoner-summoner", "enkindle", "Enkindle Bahamut", "Enkindle Phoenix", "Enkindle Solar Bahamut")
add_display_slot("summoner-summoner", "summon-ifrit", "Summon Ruby", "Summon Ifrit", "Summon Ifrit II")
add_display_slot("summoner-summoner", "summon-titan", "Summon Topaz", "Summon Titan", "Summon Titan II")
add_display_slot("summoner-summoner", "summon-garuda", "Summon Emerald", "Summon Garuda", "Summon Garuda II")
add_display_slot("redmage-redmage", "jolt", "Jolt", "Jolt II", "Jolt III")
add_display_slot("redmage-redmage", "verthunder", "Verthunder", "Verthunder III")
add_display_slot("redmage-redmage", "veraero", "Veraero", "Veraero III")
add_display_slot("redmage-redmage", "impact", "Scatter", "Impact", "Grand Impact")
add_display_slot("redmage-redmage", "fleche", "Fleche", "Vice of Thorns")


def get_display_slot(spec_slug: str, name: str) -> str:
    return DISPLAY_SLOT_ALIASES.get(spec_slug, {}).get(name) or f"{spec_slug}:{normalize_action_name(name)}"


def load_action_rows() -> dict[str, list[dict[str, str]]]:
    response = requests.get(ACTION_CSV_URL, headers={"User-Agent": USER_AGENT}, timeout=60)
    response.raise_for_status()
    rows = csv.DictReader(io.StringIO(response.content.decode("utf-8-sig")))
    by_name: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        name = row.get("Name", "").strip()
        if not name or row.get("IsPvP") == "True":
            continue
        by_name.setdefault(normalize_action_name(name), []).append(row)
    return by_name


def parse_official_actions(guide_slug: str) -> list[dict[str, str]]:
    url = f"{JOB_GUIDE_BASE_URL}/{guide_slug}/"
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
    response.raise_for_status()

    actions: list[dict[str, str]] = []
    seen: set[str] = set()
    pattern = re.compile(
        r'<a href="#([^"]+)" class="job__skill_icon js__tooltip" data-tooltip="([^"]+)"><img src="([^"]+)"'
    )
    for match in pattern.finditer(response.text):
        anchor = match.group(1)
        if anchor.startswith("pvp"):
            continue
        if not ("_action__" in anchor or anchor.startswith("pve_action__")):
            continue

        name = html.unescape(match.group(2)).strip()
        if not name or name in seen:
            continue
        seen.add(name)
        actions.append(
            {
                "anchor": anchor,
                "name": name,
                "icon_url": match.group(3),
            }
        )
    return actions


def int_field(row: dict[str, str], field: str, default: int = 0) -> int:
    try:
        return int(row.get(field, "") or default)
    except ValueError:
        return default


def choose_action_row(
    name: str,
    candidates: list[dict[str, str]],
    job_id: int,
    base_ids: list[int],
    is_role_action: bool,
) -> dict[str, str] | None:
    if not candidates:
        return None

    allowed_job_ids = {job_id, *base_ids}

    def score(row: dict[str, str]) -> tuple[int, int, int, int, int, int]:
        class_job = int_field(row, "ClassJob", -999)
        class_job_category = int_field(row, "ClassJobCategory")
        icon = int_field(row, "Icon")
        action_id = int_field(row, "#", 999999)

        return (
            1 if icon and icon != 405 else 0,
            1 if class_job in allowed_job_ids else 0,
            1 if is_role_action and row.get("IsRoleAction") == "True" else 0,
            1 if class_job_category else 0,
            1 if row.get("IsPlayerAction") == "True" else 0,
            -action_id,
        )

    return max(candidates, key=score)


def download_icon(icon_url: str, filename: str) -> None:
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    path = ICON_DIR / filename
    if path.exists() and path.stat().st_size > 0:
        return

    response = requests.get(icon_url, headers={"User-Agent": USER_AGENT}, timeout=30)
    response.raise_for_status()
    path.write_bytes(response.content)


def build_actions() -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[str]]]:
    action_rows = load_action_rows()
    output: dict[str, list[dict[str, Any]]] = {}
    skipped: dict[str, list[str]] = {}

    for spec_slug, job in JOBS.items():
        official_actions = parse_official_actions(job["guide"])
        spec_actions: list[dict[str, Any]] = []
        missing: list[str] = []

        for official_action in official_actions:
            name = official_action["name"]
            is_role_action = not official_action["anchor"].startswith("pve_action__")
            row = choose_action_row(
                name=name,
                candidates=action_rows.get(normalize_action_name(name), []),
                job_id=int(job["job_id"]),
                base_ids=list(job["base_ids"]),
                is_role_action=is_role_action,
            )
            if row is None:
                missing.append(name)
                continue

            icon = sanitize_icon_name(name)
            download_icon(official_action["icon_url"], icon)
            spec_actions.append(
                {
                    "spell_id": int_field(row, "#"),
                    "name": name,
                    "icon": icon,
                    "cooldown": int_field(row, "Recast100ms") / 10.0,
                    "duration": 0.0,
                    "level": int_field(row, "ClassJobLevel"),
                    "display_slot": get_display_slot(spec_slug, name),
                }
            )

        output[spec_slug] = spec_actions
        skipped[spec_slug] = missing
    return output, skipped


def render_python_module(actions_by_spec: dict[str, list[dict[str, Any]]], skipped: dict[str, list[str]]) -> str:
    imports = [
        "from lorgs.models.wow_spell import SpellTag",
    ]
    for job in JOBS.values():
        imports.append(f"from {job['module']} import {job['spec']}")

    spec_map = {spec_slug: JOBS[spec_slug]["spec"] for spec_slug in JOBS}

    return (
        '"""Optional full-action monitoring data generated by scripts/update_all_job_actions.py."""\n'
        "from __future__ import annotations\n\n"
        "# fmt: off\n"
        + "\n".join(imports)
        + "\n\n"
        f"ALL_ACTIONS_BY_SPEC = {pprint.pformat(actions_by_spec, width=120, sort_dicts=False)}\n\n"
        f"SKIPPED_ACTIONS_BY_SPEC = {pprint.pformat(skipped, width=120, sort_dicts=False)}\n\n"
        f"SPEC_OBJECTS = {spec_map!r}\n\n"
        + textwrap.dedent(
            """

            def _add_other_actions() -> None:
                for spec_slug, actions in ALL_ACTIONS_BY_SPEC.items():
                    spec = globals()[SPEC_OBJECTS[spec_slug]]
                    existing_ids = {spell.spell_id for spell in spec.spells}
                    existing_names = {spell.name for spell in spec.spells}
                    existing_by_id = {spell.spell_id: spell for spell in spec.spells}
                    existing_by_name = {spell.name: spell for spell in spec.spells}

                    for action in actions:
                        existing_spell = existing_by_id.get(action["spell_id"]) or existing_by_name.get(action["name"])
                        if not existing_spell:
                            continue
                        existing_spell.level = action.get("level", 0)
                        existing_spell.display_slot = action.get("display_slot", "")

                    existing_by_slot = {
                        spell.display_slot: spell
                        for spell in spec.spells
                        if getattr(spell, "display_slot", "")
                    }

                    for action in actions:
                        if action["spell_id"] in existing_ids or action["name"] in existing_names:
                            continue

                        slot_spell = existing_by_slot.get(action.get("display_slot", ""))
                        inherited_tags = list(slot_spell.tags) if slot_spell else [SpellTag.OTHER]
                        inherited_show = slot_spell.show if slot_spell and slot_spell.show is not None else False

                        spec.add_spell(
                            spell_id=action["spell_id"],
                            cooldown=action["cooldown"],
                            duration=action["duration"],
                            name=action["name"],
                            icon=action["icon"],
                            show=inherited_show,
                            tags=inherited_tags,
                            level=action.get("level", 0),
                            display_slot=action.get("display_slot", ""),
                        )
                        existing_ids.add(action["spell_id"])
                        existing_names.add(action["name"])


            _add_other_actions()
            # fmt: on
            """
        )
    )


def main() -> None:
    actions_by_spec, skipped = build_actions()
    OUTPUT_PATH.write_text(render_python_module(actions_by_spec, skipped), encoding="utf-8")

    print(f"Wrote {OUTPUT_PATH}")
    for spec_slug, actions in actions_by_spec.items():
        missing = skipped.get(spec_slug) or []
        print(f"{spec_slug}: actions={len(actions)} skipped={len(missing)}")
        if missing:
            print(f"  skipped: {', '.join(missing)}")


if __name__ == "__main__":
    main()
