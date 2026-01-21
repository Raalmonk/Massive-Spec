"""Define the Machinist Class and its Spec and Spells."""

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
MACHINIST = WowClass(id=31, name="Machinist", color="#6EE1D6")

################################################################################
# Specs
#
MACHINIST_MAIN = WowSpec(role=RDPS, wow_class=MACHINIST, name="Machinist")


################################################################################
# Spells
#

# Burst / Cooldowns
MACHINIST_MAIN.add_spell(spell_id=0, cooldown=0, name="Drill", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=0, cooldown=0, name="Air Anchor", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=0, cooldown=0, name="Chain Saw", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=0, cooldown=0, name="Barrel Stabilizer", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=0, cooldown=0, name="Wildfire", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=0, cooldown=0, name="Reassemble", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=0, cooldown=0, name="Wildfire", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=0, cooldown=0, name="Automaton Queen", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
MACHINIST_MAIN.add_spell(spell_id=0, cooldown=0, name="Second Wind", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
MACHINIST_MAIN.add_spell(spell_id=0, cooldown=0, name="Tactician", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
MACHINIST_MAIN.add_spell(spell_id=0, cooldown=0, name="Dismantle", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
