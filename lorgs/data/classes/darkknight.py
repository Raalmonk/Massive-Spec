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
DARK_KNIGHT_MAIN.add_spell(spell_id=17702, cooldown=60, name="Delirium", icon="Delirium.png", tags=[SpellTag.DAMAGE])
DARK_KNIGHT_MAIN.add_spell(spell_id=16472, cooldown=120, name="Living Shadow", icon="Living_Shadow.png", tags=[SpellTag.DAMAGE])
DARK_KNIGHT_MAIN.add_spell(spell_id=25881, cooldown=0, name="Shadowbringer", icon="Shadowbringer.png", tags=[SpellTag.DAMAGE])
DARK_KNIGHT_MAIN.add_spell(spell_id=3639, cooldown=90, name="Salted Earth", icon="Salted_Earth.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
DARK_KNIGHT_MAIN.add_spell(spell_id=36927, cooldown=120, name="Shadowed Vigil", icon="Shadowed_Vigil.png", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=3634, cooldown=60, name="Dark Mind", icon="Dark_Mind.png", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=46778, cooldown=90, name="Rampart", icon="Rampart.png", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=8779, cooldown=15, name="The Blackest Night", icon="The_Blackest_Night.png", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=25754, cooldown=60, name="Oblation", icon="Oblation.png", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=3638, cooldown=300, name="Living Dead", icon="Living_Dead.png", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=40061, cooldown=60, name="Reprisal", icon="Reprisal.png", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
DARK_KNIGHT_MAIN.add_spell(spell_id=18909, cooldown=90, name="Dark Missionary", icon="Dark_Missionary.png", tags=[SpellTag.RAID_CD])
