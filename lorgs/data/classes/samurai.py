"""Define the Samurai Class and its Spec and Spells."""

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
SAMURAI = WowClass(id=34, name="Samurai", color="#E46D04")

################################################################################
# Specs
#
SAMURAI_MAIN = WowSpec(role=MDPS, wow_class=SAMURAI, name="Samurai")


################################################################################
# Spells
#

# Burst / Cooldowns
SAMURAI_MAIN.add_spell(spell_id=41080, cooldown=55, name="Meikyo Shisui", icon="Meikyo_Shisui.png", tags=[SpellTag.DAMAGE])
SAMURAI_MAIN.add_spell(spell_id=9087, cooldown=2.5, name="Higanbana", icon="Higanbana.png", tags=[SpellTag.DAMAGE])
SAMURAI_MAIN.add_spell(spell_id=16482, cooldown=120, name="Ikishoten", icon="Ikishoten.png", tags=[SpellTag.DAMAGE])
SAMURAI_MAIN.add_spell(spell_id=7546, cooldown=45, name="True North", icon="True_North.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
SAMURAI_MAIN.add_spell(spell_id=21306, cooldown=120, name="Second Wind", icon="Second_Wind.png", tags=[SpellTag.DEFENSIVE])
SAMURAI_MAIN.add_spell(spell_id=33013, cooldown=90, name="Bloodbath", icon="Bloodbath.png", tags=[SpellTag.DEFENSIVE])
SAMURAI_MAIN.add_spell(spell_id=36962, cooldown=15, name="Tengentsu", icon="Tengentsu.png", tags=[SpellTag.DEFENSIVE])
SAMURAI_MAIN.add_spell(spell_id=28324, cooldown=90, name="Feint", icon="Feint.png", tags=[SpellTag.DEFENSIVE])
