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
MACHINIST_MAIN.add_spell(spell_id=40076, cooldown=2, name="Drill", icon="Drill.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=40078, cooldown=2, name="Air Anchor", icon="Air_Anchor.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=40082, cooldown=2, name="Chain Saw", icon="Chain_Saw.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=40080, cooldown=120, name="Barrel Stabilizer", icon="Barrel_Stabilizer.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=8855, cooldown=120, name="Wildfire", icon="Wildfire.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=2876, cooldown=55, name="Reassemble", icon="Reassemble.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=8855, cooldown=120, name="Wildfire", icon="Wildfire.png", tags=[SpellTag.DAMAGE])
MACHINIST_MAIN.add_spell(spell_id=16501, cooldown=6, name="Automaton Queen", icon="Automaton_Queen.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
MACHINIST_MAIN.add_spell(spell_id=21306, cooldown=120, name="Second Wind", icon="Second_Wind.png", tags=[SpellTag.DEFENSIVE])
MACHINIST_MAIN.add_spell(spell_id=38862, cooldown=90, name="Tactician", icon="Tactician.png", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
MACHINIST_MAIN.add_spell(spell_id=40102, cooldown=120, name="Dismantle", icon="Dismantle.png", tags=[SpellTag.RAID_CD])
