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
VIPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Reawaken", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
VIPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Vicewinder", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
VIPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Serpent's Ire", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
VIPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Uncoiled Fury", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
VIPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Second Wind", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
VIPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Bloodbath", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
VIPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Feint", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
