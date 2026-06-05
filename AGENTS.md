# FFLorrgs Agent Guidelines

## 1. Project Context & Mission
**Goal:** We are porting "Lorrgs" (a WoW cooldown planner) to "FFLorrgs" (for Final Fantasy XIV).

**Core Logic:** The codebase is heavily based on lorgs (Python/FastAPI). We are adapting the data layer to support FF14 Jobs and Encounters instead of WoW Classes and Raids.

**Data Source:** We use FF Logs API v2 (Graph QL), which is structurally identical to Warcraft Logs but uses different endpoints.

## 2. Critical "Do Not Touch" Rules
* **Legacy Code:** Do NOT delete existing WoW data files (e.g., `lorgs/data/classes/deathknight.py`) unless explicitly instructed. We use them as templates/references for the new FF14 files.
* **Comments:** Do NOT delete existing comments. This includes docstrings, inline comments, and commented-out code blocks. They often contain critical context, original Spell IDs, or logic explanations that serve as references for the porting process.
* **Architecture:** Do NOT change the core model architecture (`lorgs/models/*`) without permission. We want to reuse the existing `UserReport`, `Fight`, and `Player` logic.
* **Files:**
    * `lorgs/clients/wcl/client.py`: Ensure `URL_API` always points to `fflogs.com`, NOT `warcraftlogs.com`.

## 3. FF14 Terminology Mapping
When converting logic, map WoW terms to FF14 terms as follows:
* **Class** -> **Job** (e.g., Scholar, Paladin).
* **Spec** -> **Job** (In FF14, Class and Spec are effectively 1:1 for end-game. Treat them as the same entity).
* **Role** -> **Role** (Tank, Healer, Melee, Ranged, Caster).
* **Covenant/Soulbind** -> Ignore (FF14 has no borrowed power systems like this).
* **Hero Talents** -> Ignore (Not applicable).

## 4. Coding Standards (Python)
* **Python Version:** 3.9+
* **Formatting:** Follow black and isort configuration defined in `pyproject.toml`.
* **Line length:** 120.
* **Type Hinting:** Use strict type hints for all new functions.
* **Imports:**
    * `from lorgs.data.classes import *` structure is used heavily in this project.
    * New Job files must be registered in `lorgs/data/classes/__init__.py`.
    * New Raid/Boss files must be registered in `lorgs/data/raids/__init__.py`.

## 5. New Data File Templates
When asking to create new data, strictly follow these patterns:

**Boss Definition (`lorgs/data/raids/example_boss.py`):**
```python
from lorgs.models.raid_boss import RaidBoss
BOSS_NAME = RaidBoss(id=123, name="Boss Name", ...)
boss = BOSS_NAME
boss.add_cast(spell_id=12345, name="Mechanic Name", ...)
```

**Job Definition (`lorgs/data/classes/job_name.py`):**
```python
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
# Note: For FF14, Job is both the Class and the Spec.
JOB = WowClass(id=1, name="JobName", color="#HEX")
JOB_SPEC = WowSpec(role=ROLE, wow_class=JOB, name="JobName")
JOB_SPEC.add_spell(...)
```

## 6. Target Data & Implementation Plan (FF14)
Implementation should follow the spreadsheet data (fflorrgs.xlsx). Map the CSV columns to SpellTags as follows:

Burst/Cooldowns: SpellTag.DAMAGE (or no tag implies standard CD).

Self Mit (Self Mitigation): SpellTag.DEFENSIVE.

Raid Mit (Party Mitigation): SpellTag.RAID_CD.

Priority Job List (Dawntrail Updated)
Tanks

PLD (Paladin): Fight or Flight, Guardian, Bulwark, Holy Sheltron, Intervention, Cover, Hallowed Ground, Divine Veil, Passage of Arms.

WAR (Warrior): Inner Release, Damnation, Thrill of Battle, Bloodwhetting, Nascent Flash, Holmgang, Shake it Off.

DRK (Dark Knight): Delirium, Living Shadow, Shadowbringer, Shadowed Vigil, Dark Mind, The Blackest Night, Oblation, Living Dead, Dark Missionary.

GNB (Gunbreaker): No Mercy, Great Nebula, Camouflage, Heart of Corundum, Aurora, Superbolide, Heart of Light.

Healers

WHM (White Mage): Presence of Mind, Afflatus Misery, Temperance, Liturgy of the Bell, Divine Caress, Aquaveil, Divine Benison.

AST (Astrologian): Lightspeed, Divination, Lord of Crowns, Macrocosmos, Neutral Sect, Collective Unconscious, Sun Sign, Earthly Star, Exaltation.

SCH (Scholar): Chain Stratagem, Dissipation, Seraphism, Summon Seraph, Expedient, Fey Illumination, Sacred Soil, Protraction, Excogitation.

SGE (Sage): Psyche, Phlegma III, Zoe, Pneuma, Holos, Panhaima, Kerachole, Haima, Taurochole, Krasis.

Melee DPS

DRG (Dragoon): High Jump, Geirskougul, Lance Charge, Battle Litany, Arcane Crest (Defensive).

RPR (Reaper): Gluttony, Enshroud, Arcane Circle, Arcane Crest.

MNK (Monk): Perfect Balance, Riddle of Fire, Riddle of Wind, Brotherhood, Riddle of Earth, Mantra.

SAM (Samurai): Meikyo Shisui, Higanbana, Ikishoten, Tengentsu.

NIN (Ninja): Raiton, Kassatsu, Ten Chi Jin, Bunshin, Dokumori, Shade Shift.

VPR (Viper): Reawaken, Vicewinder, Serpent's Ire, Uncoiled Fury.

Physical Ranged DPS

BRD (Bard): Raging Strikes, Radiant Finale, Battle Voice, Troubadour, Nature's Minne.

MCH (Machinist): Drill, Air Anchor, Chain Saw, Barrel Stabilizer, Wildfire, Automaton Queen, Tactician, Dismantle.

DNC (Dancer): Standard Step, Technical Step, Devilment, Shield Samba, Curing Waltz, Improvisation.

Magical Ranged DPS

SMN (Summoner): Searing Light, Summon Bahamut/Phoenix/Solar Bahamut, Radiant Aegis.

RDM (Red Mage): Embolden, Manafication, Acceleration, Magick Barrier.

BLM (Black Mage): Ley Lines, Manafont, Manaward.

PCT (Pictomancer): Starry Muse, Striking Muse, Retribution of the Madeen, Mog of the Ages, Tempera Coat, Tempera Grassa.

(Note: Role Actions like Feint, Addle, Reprisal, Rampart should be added to each Job individually for now unless a shared Role module is established.)

## 7. Local Debug Notes
* Project-root `.env` is loaded by local debug scripts. Use `WCL_AUTH_TOKEN`, or both `WCL_CLIENT_ID` and `WCL_CLIENT_SECRET`.
* Local scripts set dummy AWS values before importing models:
  `AWS_DEFAULT_REGION=us-east-1`, `AWS_ACCESS_KEY_ID=testing`, `AWS_SECRET_ACCESS_KEY=testing`.
* Use one-command scripts for focused frontend JSON generation:
  `python scripts/debug_darkknight_fru.py`
  `python scripts/debug_astrologian_dancing_mad.py`
* `main.py` serves the frontend at `/`; the actual timeline file is `front_end/timelinev2.html`, and generated ranking data is served from `front_end/data`.

## 8. Frontend Timeline Notes
* Avoid emoji in timeline controls. Prefer short, flat text labels such as `DU`, `CD`, and `PH`, or lucide icons when an icon is clearer.
* Boss phase intervals should come from FF Logs native `phases` / `phaseTransitions` when available. Do not add hand-authored phase trigger IDs for fights whose official phases are available from FF Logs.
* Boss timeline mechanics should not render static phase/window placeholders as mechanic icons.
* Horizontal dragging is the primary timeline navigation. Keep row-selection click handling separated from drag movement so dragging does not accidentally highlight rows.
