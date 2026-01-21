"""Define the Pictomancer Class and its Spec and Spells."""

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
PICTOMANCER = WowClass(id=42, name="Pictomancer", color="#E060E0")

################################################################################
# Specs
#
PICTOMANCER_MAIN = WowSpec(role=RDPS, wow_class=PICTOMANCER, name="Pictomancer")


################################################################################
# Spells
#

# Burst / Cooldowns
PICTOMANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Holy in White", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Comet in Black", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Subtractive Palette", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Starry Muse", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Striking Muse", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Retribution of the Madeen", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Mog of the Ages", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Swiftcast", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
PICTOMANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Tempera Coat", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
PICTOMANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Addle", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
PICTOMANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Tempera Grassa", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
