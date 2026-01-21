"""Define the Dark Knight Class and its Spec and Spells."""

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
DARK_KNIGHT = WowClass(id=32, name="Dark Knight", color="#D126CC")

################################################################################
# Specs
#
DARK_KNIGHT_MAIN = WowSpec(role=TANK, wow_class=DARK_KNIGHT, name="Dark Knight")


################################################################################
# Spells
#

# Burst / Cooldowns
DARK_KNIGHT_MAIN.add_spell(spell_id=0, cooldown=0, name="Delirium", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
DARK_KNIGHT_MAIN.add_spell(spell_id=0, cooldown=0, name="Living Shadow", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
DARK_KNIGHT_MAIN.add_spell(spell_id=0, cooldown=0, name="Shadowbringer", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
DARK_KNIGHT_MAIN.add_spell(spell_id=0, cooldown=0, name="Salted Earth", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
DARK_KNIGHT_MAIN.add_spell(spell_id=0, cooldown=0, name="Shadowed Vigil", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=0, cooldown=0, name="Dark Mind", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=0, cooldown=0, name="Rampart", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=0, cooldown=0, name="The Blackest Night", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=0, cooldown=0, name="Oblation", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=0, cooldown=0, name="Living Dead", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=0, cooldown=0, name="Reprisal", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
DARK_KNIGHT_MAIN.add_spell(spell_id=0, cooldown=0, name="Dark Missionary", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
