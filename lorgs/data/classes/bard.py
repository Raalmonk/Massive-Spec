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


BARD_MAIN.add_spell(spell_id=101, cooldown=120, duration=20, name="Raging Strikes", show=False, icon="Raging_Strikes.png", tags=[SpellTag.DAMAGE])

BARD_MAIN.add_spell(spell_id=118, cooldown=120, duration=15, name="Battle Voice", show=True, icon="Battle_Voice.png", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=25785, cooldown=110, duration=15, name="Radiant Finale", show=False, icon="Radiant_Finale.png", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=3559, cooldown=120, name="The Wanderer's Minuet", show=True, icon="The_Wanderer's_Minuet.png", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=114, cooldown=120, name="Mage's Ballad", icon="Mage's_Ballad.png",show=True,  tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=116, cooldown=120, name="Army's Paeon",show=True,  icon="Army's_Paeon.png", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=16496, cooldown=2.5, name="Apex Arrow", show=True, icon="Apex_Arrow.png", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=3562, cooldown=60, name="Sidewinder", icon="Sidewinder.png",show=False, tags=[SpellTag.DAMAGE])
# Self Mitigation
BARD_MAIN.add_spell(spell_id=7541, cooldown=120, name="Second Wind", icon="Second_Wind.png",show=False,  tags=[SpellTag.DEFENSIVE])


# Party Mitigation
BARD_MAIN.add_spell(spell_id=7405, cooldown=90, duration=15, name="Troubadour", icon="Troubadour.png",show=True,  tags=[SpellTag.RAID_CD])
BARD_MAIN.add_spell(spell_id=7408, cooldown=120, duration=15, name="Nature's Minne", icon="Nature's_Minne.png",show=False,  tags=[SpellTag.RAID_CD])
