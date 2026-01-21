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
SAMURAI_MAIN.add_spell(spell_id=0, cooldown=0, name="Meikyo Shisui", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SAMURAI_MAIN.add_spell(spell_id=0, cooldown=0, name="Higanbana", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SAMURAI_MAIN.add_spell(spell_id=0, cooldown=0, name="Ikishoten", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SAMURAI_MAIN.add_spell(spell_id=0, cooldown=0, name="True North", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
SAMURAI_MAIN.add_spell(spell_id=0, cooldown=0, name="Second Wind", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
SAMURAI_MAIN.add_spell(spell_id=0, cooldown=0, name="Bloodbath", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
SAMURAI_MAIN.add_spell(spell_id=0, cooldown=0, name="Tengentsu", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
SAMURAI_MAIN.add_spell(spell_id=0, cooldown=0, name="Feint", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
