"""Define the Warrior Class and its Spec and Spells."""

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
WARRIOR = WowClass(id=21, name="Warrior", color="#CF2621")

################################################################################
# Specs
#
WARRIOR_MAIN = WowSpec(role=TANK, wow_class=WARRIOR, name="Warrior")


################################################################################
# Spells
#

# Burst / Cooldowns
WARRIOR_MAIN.add_spell(spell_id=8768, cooldown=60, name="Inner Release", icon="Inner_Release.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
WARRIOR_MAIN.add_spell(spell_id=36923, cooldown=120, name="Damnation", icon="Damnation.png", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=29297, cooldown=90, name="Thrill of Battle", icon="Thrill_of_Battle.png", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=46778, cooldown=90, name="Rampart", icon="Rampart.png", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=25751, cooldown=25, name="Bloodwhetting", icon="Bloodwhetting.png", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=17889, cooldown=25, name="Nascent Flash", icon="Nascent_Flash.png", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=29298, cooldown=240, name="Holmgang", icon="Holmgang.png", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=40061, cooldown=60, name="Reprisal", icon="Reprisal.png", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
WARRIOR_MAIN.add_spell(spell_id=17699, cooldown=90, name="Shake It Off", icon="Shake_It_Off.png", tags=[SpellTag.RAID_CD])
