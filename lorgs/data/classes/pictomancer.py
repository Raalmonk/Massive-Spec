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
PICTOMANCER_MAIN.add_spell(spell_id=47126, cooldown=2, name="Holy in White", icon="Holy_in_White.png", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=47127, cooldown=2, name="Comet in Black", icon="Comet_in_Black.png", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=47125, cooldown=1, name="Subtractive Palette", icon="Subtractive_Palette.png", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=47144, cooldown=120, name="Starry Muse", icon="Starry_Muse.png", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=47139, cooldown=60, name="Striking Muse", icon="Striking_Muse.png", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=47137, cooldown=30, name="Retribution of the Madeen", icon="Retribution_of_the_Madeen.png", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=47136, cooldown=30, name="Mog of the Ages", icon="Mog_of_the_Ages.png", tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=30926, cooldown=40, name="Swiftcast", icon="Swiftcast.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
PICTOMANCER_MAIN.add_spell(spell_id=47112, cooldown=120, name="Tempera Coat", icon="Tempera_Coat.png", tags=[SpellTag.DEFENSIVE])
PICTOMANCER_MAIN.add_spell(spell_id=40060, cooldown=90, name="Addle", icon="Addle.png", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
PICTOMANCER_MAIN.add_spell(spell_id=39833, cooldown=1, name="Tempera Grassa", icon="Tempera_Grassa.png", tags=[SpellTag.RAID_CD])
