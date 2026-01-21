"""Define the Dragoon Class and its Spec and Spells."""

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
DRAGOON = WowClass(id=22, name="Dragoon", color="#4164CD")

################################################################################
# Specs
#
DRAGOON_MAIN = WowSpec(role=MDPS, wow_class=DRAGOON, name="Dragoon")


################################################################################
# Spells
#

# Burst / Cooldowns
DRAGOON_MAIN.add_spell(spell_id=36911, cooldown=30, name="High Jump", icon="High_Jump.png", tags=[SpellTag.DAMAGE])
DRAGOON_MAIN.add_spell(spell_id=36913, cooldown=60, name="Geirskogul", icon="Geirskogul.png", tags=[SpellTag.DAMAGE])
DRAGOON_MAIN.add_spell(spell_id=29310, cooldown=60, name="Lance Charge", icon="Lance_Charge.png", tags=[SpellTag.DAMAGE])
DRAGOON_MAIN.add_spell(spell_id=9640, cooldown=120, name="Battle Litany", icon="Battle_Litany.png", tags=[SpellTag.DAMAGE])
DRAGOON_MAIN.add_spell(spell_id=7546, cooldown=45, name="True North", icon="True_North.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
DRAGOON_MAIN.add_spell(spell_id=21306, cooldown=120, name="Second Wind", icon="Second_Wind.png", tags=[SpellTag.DEFENSIVE])
DRAGOON_MAIN.add_spell(spell_id=33013, cooldown=90, name="Bloodbath", icon="Bloodbath.png", tags=[SpellTag.DEFENSIVE])
DRAGOON_MAIN.add_spell(spell_id=28324, cooldown=90, name="Feint", icon="Feint.png", tags=[SpellTag.DEFENSIVE])
