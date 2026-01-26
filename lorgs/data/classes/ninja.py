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
NINJA_MAIN.add_spell(spell_id=36957, cooldown=120, duration=20, name="Dokumori", show=True,icon="Dokumori.png", tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=7403, cooldown=120, name="Ten Chi Jin", icon="Ten_Chi_Jin.png",show=False,  tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=16493, cooldown=90, name="Bunshin",show=True, icon="Bunshin.png", tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=2264, cooldown=60, name="Kassatsu",show=True, icon="Kassatsu.png", tags=[SpellTag.DAMAGE])


NINJA_MAIN.add_spell(spell_id=2267, name="Raiton", icon="Raiton.png",show=False, tags=[SpellTag.DAMAGE])
NINJA_MAIN.add_spell(spell_id=7546, cooldown=45, duration=10, name="True North",show=True, icon="True_North.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
NINJA_MAIN.add_spell(spell_id=7541, cooldown=120, name="Second Wind", icon="Second_Wind.png", show=False, tags=[SpellTag.DEFENSIVE])
NINJA_MAIN.add_spell(spell_id=7542, cooldown=90, duration=20, name="Bloodbath", show=False, icon="Bloodbath.png", tags=[SpellTag.DEFENSIVE])
NINJA_MAIN.add_spell(spell_id=2241, cooldown=120, name="Shade Shift", icon="Shade_Shift.png", show=False, tags=[SpellTag.DEFENSIVE])

NINJA_MAIN.add_spell(spell_id=7549, cooldown=90, duration=15, name="Feint",show=True, icon="Feint.png", tags=[SpellTag.RAID_CD])
