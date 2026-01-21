"""Define the Bard Class and its Spec and Spells."""

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
BARD = WowClass(id=23, name="Bard", color="#91BA5E")

################################################################################
# Specs
#
BARD_MAIN = WowSpec(role=RDPS, wow_class=BARD, name="Bard")


################################################################################
# Spells
#

# Burst / Cooldowns
BARD_MAIN.add_spell(spell_id=16496, cooldown=2.5, name="Apex Arrow", icon="Apex_Arrow.png", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=3562, cooldown=60, name="Sidewinder", icon="Sidewinder.png", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=101, cooldown=120, name="Raging Strikes", icon="Raging_Strikes.png", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=25785, cooldown=110, name="Radiant Finale", icon="Radiant_Finale.png", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=118, cooldown=120, name="Battle Voice", icon="Battle_Voice.png", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=8843, cooldown=120, name="The Wanderer's Minuet", icon="The_Wanderer's_Minuet.png", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=114, cooldown=120, name="Mage's Ballad", icon="Mage's_Ballad.png", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=116, cooldown=120, name="Army's Paeon", icon="Army's_Paeon.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
BARD_MAIN.add_spell(spell_id=57, cooldown=120, name="Second Wind", icon="Second_Wind.png", tags=[SpellTag.DEFENSIVE])
BARD_MAIN.add_spell(spell_id=7405, cooldown=90, name="Troubadour", icon="Troubadour.png", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
BARD_MAIN.add_spell(spell_id=7408, cooldown=120, name="Nature's Minne", icon="Nature's_Minne.png", tags=[SpellTag.RAID_CD])
