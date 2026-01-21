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
NINJA_MAIN.add_spell(spell_id=0, cooldown=0, name="Raiton", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=0, cooldown=0, name="Kassatsu", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=0, cooldown=0, name="Ten Chi Jin", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=0, cooldown=0, name="Bunshin", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=0, cooldown=0, name="Dokumori", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=0, cooldown=0, name="True North", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
NINJA_MAIN.add_spell(spell_id=0, cooldown=0, name="Second Wind", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
NINJA_MAIN.add_spell(spell_id=0, cooldown=0, name="Bloodbath", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
NINJA_MAIN.add_spell(spell_id=0, cooldown=0, name="Shade Shift", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
NINJA_MAIN.add_spell(spell_id=0, cooldown=0, name="Feint", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
