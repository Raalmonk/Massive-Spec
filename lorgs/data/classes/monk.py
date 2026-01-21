"""Define the Monk Class and its Spec and Spells."""

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
MONK = WowClass(id=20, name="Monk", color="#D69C00")

################################################################################
# Specs
#
MONK_MAIN = WowSpec(role=MDPS, wow_class=MONK, name="Monk")


################################################################################
# Spells
#

# Burst / Cooldowns
MONK_MAIN.add_spell(spell_id=69, cooldown=40, name="Perfect Balance", icon="Perfect_Balance.png", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=7395, cooldown=60, name="Riddle of Fire", icon="Riddle_of_Fire.png", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=7868, cooldown=90, name="Riddle of Wind", icon="Riddle_of_Wind.png", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=7396, cooldown=120, name="Brotherhood", icon="Brotherhood.png", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=7546, cooldown=45, name="True North", icon="True_North.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
MONK_MAIN.add_spell(spell_id=57, cooldown=120, name="Second Wind", icon="Second_Wind.png", tags=[SpellTag.DEFENSIVE])
MONK_MAIN.add_spell(spell_id=34, cooldown=90, name="Bloodbath", icon="Bloodbath.png", tags=[SpellTag.DEFENSIVE])
MONK_MAIN.add_spell(spell_id=7394, cooldown=120, name="Riddle of Earth", icon="Riddle_of_Earth.png", tags=[SpellTag.DEFENSIVE])
MONK_MAIN.add_spell(spell_id=76, cooldown=90, name="Feint", icon="Feint.png", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
MONK_MAIN.add_spell(spell_id=65, cooldown=90, name="Mantra", icon="Mantra.png", tags=[SpellTag.RAID_CD])
