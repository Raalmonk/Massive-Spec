FFLorrgs Agent Guidelines
1. Project Context & Mission
Goal: We are porting "Lorrgs" (a WoW cooldown planner) to "FFLorrgs" (for Final Fantasy XIV).

Core Logic: The codebase is heavily based on lorgs (Python/FastAPI). We are adapting the data layer to support FF14 Jobs and Encounters instead of WoW Classes and Raids.

Data Source: We use FF Logs API v2 (Graph QL), which is structurally identical to Warcraft Logs but uses different endpoints.

2. Critical "Do Not Touch" Rules
Legacy Code: Do NOT delete existing WoW data files (e.g., lorgs/data/classes/deathknight.py) unless explicitly instructed. We use them as templates/references for the new FF14 files.

Comments: Do NOT delete existing comments. This includes docstrings, inline comments, and commented-out code blocks. They often contain critical context, original Spell IDs, or logic explanations that serve as references for the porting process.

Architecture: Do NOT change the core model architecture (lorgs/models/*) without permission. We want to reuse the existing UserReport, Fight, and Player logic.

Files:

lorgs/clients/wcl/client.py: Ensure URL_API always points to fflogs.com, NOT warcraftlogs.com.

3. FF14 Terminology Mapping
When converting logic, map WoW terms to FF14 terms as follows:

Class -> Job (e.g., Scholar, Paladin).

Spec -> Job (In FF14, Class and Spec are effectively 1:1 for end-game. Treat them as the same entity).

Role -> Role (Tank, Healer, Melee, Ranged, Caster).

Covenant/Soulbind -> Ignore (FF14 has no borrowed power systems like this).

Hero Talents -> Ignore (Not applicable).

4. Coding Standards (Python)
Python Version: 3.9+

Formatting: Follow black and isort configuration defined in pyproject.toml.

Line length: 120.

Type Hinting: Use strict type hints for all new functions.

Imports:

from lorgs.data.classes import * structure is used heavily in this project.

New Job files must be registered in lorgs/data/classes/__init__.py.

New Raid/Boss files must be registered in lorgs/data/raids/__init__.py.

5. New Data File Templates
When asking to create new data, strictly follow these patterns:

Boss Definition (lorgs/data/raids/example_boss.py):

Python

from lorgs.models.raid_boss import RaidBoss
BOSS_NAME = RaidBoss(id=123, name="Boss Name", ...)
boss = BOSS_NAME
boss.add_cast(spell_id=12345, name="Mechanic Name", ...)
Job Definition (lorgs/data/classes/job_name.py):

Python

from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
JOB = WowClass(id=1, name="JobName", color="#HEX")
JOB_SPEC = WowSpec(role=ROLE, wow_class=JOB, name="JobName")
JOB_SPEC.add_spell(...)