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
WARRIOR_MAIN.add_spell(spell_id=0, cooldown=0, name="Inner Release", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
WARRIOR_MAIN.add_spell(spell_id=0, cooldown=0, name="Damnation", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=0, cooldown=0, name="Thrill of Battle", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=0, cooldown=0, name="Rampart", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=0, cooldown=0, name="Bloodwhetting", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=0, cooldown=0, name="Nascent Flash", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=0, cooldown=0, name="Holmgang", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
WARRIOR_MAIN.add_spell(spell_id=0, cooldown=0, name="Reprisal", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
WARRIOR_MAIN.add_spell(spell_id=0, cooldown=0, name="Shake it Off", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
