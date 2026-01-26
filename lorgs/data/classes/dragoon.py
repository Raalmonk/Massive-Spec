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
DRAGOON_MAIN.add_spell(spell_id=3557, cooldown=120, duration=20, name="Battle Litany", show=True, icon="Battle_Litany.png", tags=[SpellTag.DAMAGE])

DRAGOON_MAIN.add_spell(spell_id=3555, cooldown=60, duration=20, name="Geirskogul",show=True, icon="Geirskogul.png", tags=[SpellTag.DAMAGE])
DRAGOON_MAIN.add_spell(spell_id=16478, cooldown=30, name="High Jump", icon="High_Jump.png",show=True, tags=[SpellTag.DAMAGE])
DRAGOON_MAIN.add_spell(spell_id=85, cooldown=60, name="Lance Charge", icon="Lance_Charge.png", show=False, tags=[SpellTag.DAMAGE])

DRAGOON_MAIN.add_spell(spell_id=7546, cooldown=45, duration=10, name="True North", icon="True_North.png",show=True, tags=[SpellTag.DAMAGE])

# Self Mitigation
DRAGOON_MAIN.add_spell(spell_id=7541, cooldown=120, name="Second Wind", icon="Second_Wind.png", show=False, tags=[SpellTag.DEFENSIVE])
DRAGOON_MAIN.add_spell(spell_id=7542, cooldown=7542, duration=20, name="Bloodbath", icon="Bloodbath.png", show=False, tags=[SpellTag.DEFENSIVE])
DRAGOON_MAIN.add_spell(spell_id=7549, cooldown=7549, duration=15, name="Feint", icon="Feint.png",show=True, tags=[SpellTag.RAID_CD])
