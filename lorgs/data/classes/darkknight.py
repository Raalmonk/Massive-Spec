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
DARK_KNIGHT_MAIN.add_spell(spell_id=16472, cooldown=120, name="Living Shadow", show=True, icon="Living_Shadow.png", tags=[SpellTag.DAMAGE])
DARK_KNIGHT_MAIN.add_spell(spell_id=7390, cooldown=60, name="Delirium", show=True, icon="Delirium.png", tags=[SpellTag.DAMAGE])
DARK_KNIGHT_MAIN.add_spell(spell_id=3639, cooldown=90, duration=15, name="Salted Earth", show=True, icon="Salted_Earth.png", tags=[SpellTag.DAMAGE])
DARK_KNIGHT_MAIN.add_spell(spell_id=25757, cooldown=60, name="Shadowbringer", show=False, icon="Shadowbringer.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
DARK_KNIGHT_MAIN.add_spell(spell_id=36927, cooldown=120, duration=15, name="Shadowed Vigil", show=True, icon="Shadowed_Vigil.png", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=7531, cooldown=90, duration=20, name="Rampart", show=True, icon="Rampart.png", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=3634, cooldown=60, duration=10, name="Dark Mind", show=True, icon="Dark_Mind.png", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=7393, cooldown=15, name="The Blackest Night", show=False, icon="The_Blackest_Night.png", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=25754, cooldown=60, duration=10, name="Oblation", show=False, icon="Oblation.png", tags=[SpellTag.DEFENSIVE])
DARK_KNIGHT_MAIN.add_spell(spell_id=3638, cooldown=300, duration=10, name="Living Dead", show=True, icon="Living_Dead.png", tags=[SpellTag.DEFENSIVE])


# Party Mitigation
DARK_KNIGHT_MAIN.add_spell(spell_id=7535, cooldown=60, duration=15, name="Reprisal", show=True,  icon="Reprisal.png", tags=[SpellTag.RAID_CD])
DARK_KNIGHT_MAIN.add_spell(spell_id=16471, cooldown=90, duration=15, name="Dark Missionary", show=True, icon="Dark_Missionary.png", tags=[SpellTag.RAID_CD])