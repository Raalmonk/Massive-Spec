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
GUNBREAKER_MAIN.add_spell(spell_id=0, cooldown=0, name="No Mercy", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
GUNBREAKER_MAIN.add_spell(spell_id=0, cooldown=0, name="Bloodfest", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
GUNBREAKER_MAIN.add_spell(spell_id=0, cooldown=0, name="Great Nebula", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
GUNBREAKER_MAIN.add_spell(spell_id=0, cooldown=0, name="Camouflage", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
GUNBREAKER_MAIN.add_spell(spell_id=0, cooldown=0, name="Rampart", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
GUNBREAKER_MAIN.add_spell(spell_id=0, cooldown=0, name="Heart of Corundum", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
GUNBREAKER_MAIN.add_spell(spell_id=0, cooldown=0, name="Aurora", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
GUNBREAKER_MAIN.add_spell(spell_id=0, cooldown=0, name="Superbolide", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
GUNBREAKER_MAIN.add_spell(spell_id=0, cooldown=0, name="Reprisal", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
GUNBREAKER_MAIN.add_spell(spell_id=0, cooldown=0, name="Heart of Light", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
