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
MONK_MAIN.add_spell(spell_id=69, cooldown=40, name="Perfect Balance",show=True, icon="Perfect_Balance.png", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=7395, cooldown=60, duration=20, name="Riddle of Fire",show=True, icon="Riddle_of_Fire.png", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=25766, cooldown=90, duration=15, name="Riddle of Wind",show=True, icon="Riddle_of_Wind.png", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=7396, cooldown=120, duration=20, name="Brotherhood",show=True, icon="Brotherhood.png", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=7546, cooldown=45, duration=10, name="True North",show=True, icon="True_North.png", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=25768, name="Rising Phoenix",show=True, icon="Rising_Phoenix.png", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=25769, name="Phantom Rush",show=True, icon="Phantom_Rush.png", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=36948, name="Elixir Burst",show=True, icon="Elixir_Burst.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
MONK_MAIN.add_spell(spell_id=7541, cooldown=120, name="Second Wind", icon="Second_Wind.png", show=False,tags=[SpellTag.DEFENSIVE])
MONK_MAIN.add_spell(spell_id=7542, cooldown=90, duration=20, name="Bloodbath", icon="Bloodbath.png",show=False, tags=[SpellTag.DEFENSIVE])
MONK_MAIN.add_spell(spell_id=7394, cooldown=120, duration=10, name="Riddle of Earth", icon="Riddle_of_Earth.png",show=False, tags=[SpellTag.DEFENSIVE])
MONK_MAIN.add_spell(spell_id=7549, cooldown=90, duration=15, name="Feint", icon="Feint.png",show=True, tags=[SpellTag.RAID_CD])

# Party Mitigation
MONK_MAIN.add_spell(spell_id=65, cooldown=90, duration=15, name="Mantra", icon="Mantra.png",show=False, tags=[SpellTag.RAID_CD])
