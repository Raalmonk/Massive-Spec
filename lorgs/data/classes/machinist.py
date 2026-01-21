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
MACHINIST_MAIN.add_spell(spell_id=16498, cooldown=20, name="Drill", icon="Drill.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=16500, cooldown=40, name="Air Anchor", icon="Air_Anchor.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=25788, cooldown=60, name="Chain Saw", icon="Chain_Saw.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=7414, cooldown=120, name="Barrel Stabilizer", icon="Barrel_Stabilizer.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=2878, cooldown=120, name="Wildfire", icon="Wildfire.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=2876, cooldown=55, name="Reassemble", icon="Reassemble.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=2878, cooldown=120, name="Wildfire", icon="Wildfire.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=16501, cooldown=6, name="Automaton Queen", icon="Automaton_Queen.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
MACHINIST_MAIN.add_spell(spell_id=57, cooldown=120, name="Second Wind", icon="Second_Wind.png", tags=[SpellTag.DEFENSIVE])
MACHINIST_MAIN.add_spell(spell_id=7555, cooldown=90, name="Tactician", icon="Tactician.png", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
MACHINIST_MAIN.add_spell(spell_id=2887, cooldown=120, name="Dismantle", icon="Dismantle.png", tags=[SpellTag.RAID_CD])
