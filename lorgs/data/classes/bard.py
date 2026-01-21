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
BARD_MAIN.add_spell(spell_id=0, cooldown=0, name="Apex Arrow", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=0, cooldown=0, name="Sidewinder", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=0, cooldown=0, name="Raging Strikes", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=0, cooldown=0, name="Radiant Finale", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=0, cooldown=0, name="Battle Voice", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=0, cooldown=0, name="The Wanderer's Minuet", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=0, cooldown=0, name="Mage's Ballad", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BARD_MAIN.add_spell(spell_id=0, cooldown=0, name="Army's Paeon", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
BARD_MAIN.add_spell(spell_id=0, cooldown=0, name="Second Wind", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
BARD_MAIN.add_spell(spell_id=0, cooldown=0, name="Troubadour", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
BARD_MAIN.add_spell(spell_id=0, cooldown=0, name="Nature's Minne", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
