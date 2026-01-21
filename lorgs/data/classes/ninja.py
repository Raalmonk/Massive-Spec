"""Define the Ninja Class and its Spec and Spells."""

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
NINJA = WowClass(id=30, name="Ninja", color="#AF1964")

################################################################################
# Specs
#
NINJA_MAIN = WowSpec(role=MDPS, wow_class=NINJA, name="Ninja")


################################################################################
# Spells
#

# Burst / Cooldowns
NINJA_MAIN.add_spell(spell_id=41109, cooldown=1.5, name="Raiton", icon="Raiton.png", tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=2264, cooldown=60, name="Kassatsu", icon="Kassatsu.png", tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=7403, cooldown=120, name="Ten Chi Jin", icon="Ten_Chi_Jin.png", tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=33662, cooldown=90, name="Bunshin", icon="Bunshin.png", tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=36957, cooldown=120, name="Dokumori", icon="Dokumori.png", tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=7546, cooldown=45, name="True North", icon="True_North.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
NINJA_MAIN.add_spell(spell_id=21306, cooldown=120, name="Second Wind", icon="Second_Wind.png", tags=[SpellTag.DEFENSIVE])
NINJA_MAIN.add_spell(spell_id=33013, cooldown=90, name="Bloodbath", icon="Bloodbath.png", tags=[SpellTag.DEFENSIVE])
NINJA_MAIN.add_spell(spell_id=2241, cooldown=120, name="Shade Shift", icon="Shade_Shift.png", tags=[SpellTag.DEFENSIVE])
NINJA_MAIN.add_spell(spell_id=28324, cooldown=90, name="Feint", icon="Feint.png", tags=[SpellTag.DEFENSIVE])
