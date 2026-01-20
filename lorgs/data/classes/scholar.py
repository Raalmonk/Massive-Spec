# lorgs/data/classes/scholar.py
from lorgs.data.constants import *
from lorgs.data.roles import *
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag, WowSpell

# Define the Class (Color: FFLogs Scholar Purple)
SCHOLAR = WowClass(id=28, name="Scholar", color="#8657FF")

# Define the Spec (Role: Healer)
SCHOLAR_MAIN = WowSpec(role=HEAL, wow_class=SCHOLAR, name="Scholar")

# --- Spells ---

# Chain Stratagem (Debuff, 15s duration, 120s CD)
SCHOLAR_MAIN.add_debuff(
    spell_id=7436,
    cooldown=120,
    duration=15,
    name="Chain Stratagem",
    icon="sch_chain_stratagem.jpg",
    tags=[SpellTag.RAID_CD]
)

# Expedient (Buff, 20s duration, 120s CD)
SCHOLAR_MAIN.add_spell(
    spell_id=25868,
    cooldown=120,
    duration=20,
    name="Expedient",
    icon="sch_expedient.jpg",
    tags=[SpellTag.RAID_CD, SpellTag.MOVE]
)

# Dissipation (Buff, 30s duration, 180s CD)
SCHOLAR_MAIN.add_spell(
    spell_id=3587,
    cooldown=180,
    duration=30,
    name="Dissipation",
    icon="sch_dissipation.jpg"
)

# Summon Seraph (Pet/Buff, 22s duration, 120s CD)
SCHOLAR_MAIN.add_spell(
    spell_id=16545,
    cooldown=120,
    duration=22,
    name="Summon Seraph",
    icon="sch_summon_seraph.jpg",
    tags=[SpellTag.RAID_CD]
)
