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
PICTOMANCER_MAIN.add_spell(spell_id=34675, cooldown=120, duration=20, name="Starry Muse", icon="Starry_Muse.png",show=True,  tags=[SpellTag.DAMAGE])

PICTOMANCER_MAIN.add_spell(spell_id=34683, cooldown=1, name="Subtractive Palette", icon="Subtractive_Palette.png", show=True, tags=[SpellTag.DAMAGE])

PICTOMANCER_MAIN.add_spell(spell_id=34674, cooldown=60, name="Striking Muse", icon="Striking_Muse.png",show=True,  tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=34677, cooldown=30, name="Retribution of the Madeen", icon="Retribution_of_the_Madeen.png", show=False, tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=34676, cooldown=30, name="Mog of the Ages", icon="Mog_of_the_Ages.png", show=False, tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=7561, cooldown=40, name="Swiftcast", icon="Swiftcast.png", show=False, tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=34662, cooldown=2.5, name="Holy in White", icon="Holy_in_White.png", show=False, tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=34663, cooldown=3.3, name="Comet in Black", icon="Comet_in_Black.png", show=False, tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=34653, cooldown=0.0, name="Blizzard in Cyan", icon="Blizzard_in_Cyan.png", show=True, tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=34650, cooldown=0.0, name="Fire in Red", icon="Fire_in_Red.png", show=False, tags=[SpellTag.DAMAGE])


PICTOMANCER_MAIN.add_spell(spell_id=34664, cooldown=0.0, name="Pom Motif", icon="Pom_Motif.png", show=False, tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=34665, cooldown=0.0, name="Wing Motif", icon="Wing_Motif.png", show=False, tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=34666, cooldown=0.0, name="Claw Motif", icon="Claw_Motif.png", show=False, tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=34667, cooldown=0.0, name="Maw Motif", icon="Maw_Motif.png", show=False, tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=34668, cooldown=0.0, name="Hammer Motif", icon="Hammer_Motif.png", show=False, tags=[SpellTag.DAMAGE])
PICTOMANCER_MAIN.add_spell(spell_id=34669, cooldown=0.0, name="Starry Sky Motif", icon="Starry_Sky_Motif.png", show=False, tags=[SpellTag.DAMAGE])


# Self Mitigation
PICTOMANCER_MAIN.add_spell(spell_id=34685, cooldown=120, duration=10, name="Tempera Coat", icon="Tempera_Coat.png", show=False, tags=[SpellTag.DEFENSIVE])


# Party Mitigation
PICTOMANCER_MAIN.add_spell(spell_id=7560, cooldown=90, duration=15, name="Addle", icon="Addle.png", show=True, tags=[SpellTag.RAID_CD])
PICTOMANCER_MAIN.add_spell(spell_id=34686, cooldown=1, duration=10, name="Tempera Grassa", icon="Tempera_Grassa.png", show=False, tags=[SpellTag.RAID_CD])
