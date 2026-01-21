"""Define the Viper Class and its Spec and Spells."""

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
VIPER = WowClass(id=41, name="Viper", color="#108010")

################################################################################
# Specs
#
VIPER_MAIN = WowSpec(role=MDPS, wow_class=VIPER, name="Viper")


################################################################################
# Spells
#

# Burst / Cooldowns
VIPER_MAIN.add_spell(spell_id=38801, cooldown=0, name="Reawaken", icon="Reawaken.png", tags=[SpellTag.DAMAGE])
VIPER_MAIN.add_spell(spell_id=34620, cooldown=40, name="Vicewinder", icon="Vicewinder.png", tags=[SpellTag.DAMAGE])
VIPER_MAIN.add_spell(spell_id=34647, cooldown=120, name="Serpent's Ire", icon="Serpent's_Ire.png", tags=[SpellTag.DAMAGE])
VIPER_MAIN.add_spell(spell_id=34633, cooldown=3.5, name="Uncoiled Fury", icon="Uncoiled_Fury.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
VIPER_MAIN.add_spell(spell_id=21306, cooldown=120, name="Second Wind", icon="Second_Wind.png", tags=[SpellTag.DEFENSIVE])
VIPER_MAIN.add_spell(spell_id=33013, cooldown=90, name="Bloodbath", icon="Bloodbath.png", tags=[SpellTag.DEFENSIVE])
VIPER_MAIN.add_spell(spell_id=28324, cooldown=90, name="Feint", icon="Feint.png", tags=[SpellTag.DEFENSIVE])
