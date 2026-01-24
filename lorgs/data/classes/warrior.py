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
WARRIOR_MAIN.add_spell(spell_id=7389, cooldown=60, name="Inner Release", show=True, icon="Inner_Release.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
WARRIOR_MAIN.add_spell(spell_id=36923, cooldown=120, name="Damnation", duration=15, show=True, icon="Damnation.png", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=7531, cooldown=90, duration=20, name="Rampart", show=True, icon="Rampart.png", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=40, cooldown=90, duration=10,name="Thrill of Battle", show=True, icon="Thrill_of_Battle.png", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=25751, cooldown=25, name="Bloodwhetting", show=False, icon="Bloodwhetting.png", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=16464, cooldown=25, name="Nascent Flash", show=False, icon="Nascent_Flash.png", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=43, cooldown=240, name="Holmgang", duration=10,show=True, icon="Holmgang.png", tags=[SpellTag.DEFENSIVE])


# Party Mitigation
WARRIOR_MAIN.add_spell(spell_id=7535, cooldown=60, duration=15,name="Reprisal", show=True, icon="Reprisal.png", tags=[SpellTag.RAID_CD])
WARRIOR_MAIN.add_spell(spell_id=7388, cooldown=90, name="Shake It Off", show=True, icon="Shake_It_Off.png", tags=[SpellTag.RAID_CD])
