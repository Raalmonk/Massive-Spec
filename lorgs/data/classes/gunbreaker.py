"""Define the Gunbreaker Class and its Spec and Spells."""

# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import *
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


################################################################################
# Class
#
GUNBREAKER = WowClass(id=37, name="Gunbreaker", color="#796D30")

################################################################################
# Specs
#
GUNBREAKER_MAIN = WowSpec(role=TANK, wow_class=GUNBREAKER, name="Gunbreaker")


################################################################################
# Spells
#

# Burst / Cooldowns
GUNBREAKER_MAIN.add_spell(spell_id=16138, cooldown=60, duration=20, name="No Mercy",show=True, icon="No_Mercy.png", tags=[SpellTag.DAMAGE])
GUNBREAKER_MAIN.add_spell(spell_id=16164, cooldown=60, name="Bloodfest", icon="Bloodfest.png",show=True, tags=[SpellTag.DAMAGE])

# Self Mitigation
GUNBREAKER_MAIN.add_spell(spell_id=36935, cooldown=120, duration=15, name="Great Nebula",show=True, icon="Great_Nebula.png", tags=[SpellTag.DEFENSIVE])
GUNBREAKER_MAIN.add_spell(spell_id=7531, cooldown=90, duration=20, name="Rampart",show=True, icon="Rampart.png", tags=[SpellTag.DEFENSIVE])
GUNBREAKER_MAIN.add_spell(spell_id=16140, cooldown=90, duration=20, name="Camouflage",show=True, icon="Camouflage.png", tags=[SpellTag.DEFENSIVE])
GUNBREAKER_MAIN.add_spell(spell_id=25758, cooldown=25, duration=8, name="Heart of Corundum",show=False, icon="Heart_of_Corundum.png", tags=[SpellTag.DEFENSIVE])
GUNBREAKER_MAIN.add_spell(spell_id=16151, cooldown=60, duration=18, name="Aurora",show=False, icon="Aurora.png", tags=[SpellTag.DEFENSIVE])
GUNBREAKER_MAIN.add_spell(spell_id=16152, cooldown=360, duration=10, name="Superbolide",show=True, icon="Superbolide.png", tags=[SpellTag.DEFENSIVE])


# Party Mitigation
GUNBREAKER_MAIN.add_spell(spell_id=16160, cooldown=90, duration=15, name="Heart of Light",show=True, icon="Heart_of_Light.png", tags=[SpellTag.RAID_CD])
GUNBREAKER_MAIN.add_spell(spell_id=7535, cooldown=60, duration=15, name="Reprisal",show=True, icon="Reprisal.png", tags=[SpellTag.RAID_CD])