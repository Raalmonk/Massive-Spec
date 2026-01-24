"""Define Consumeables/Potions players can use."""

# pylint: disable=line-too-long
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import


from lorgs.data.classes import *
from lorgs.models.wow_potion import WowPotion
from lorgs.models.wow_spell import WowSpell
from lorgs.models.wow_spell import SpellTag


################################################################################
# Heal Potions
#

# generic pots for all specs


################################################################################
# DPS Potions
#

# Grade 4 Gemdraught of Intelligence [HQ]
potion_int = WowPotion(
    spell_id=34603669,
    cooldown=270,
    duration=30,
    color="#b576e8",
    name="Grade 4 Gemdraught of Intelligence [HQ]",
    icon="Grade_4_gemdraught_of_intelligence_icon1.png",
    tags=[SpellTag.UTILITY],
    item=49237,
)

CASTER_SPECS = [RED_MAGE_MAIN, SUMMONER_MAIN, BLACK_MAGE_MAIN, PICTOMANCER_MAIN]
potion_int.add_specs(*CASTER_SPECS)


# Grade 4 Gemdraught of Dexterity
potion_dex = WowPotion(
    spell_id=34603667,
    cooldown=270,
    duration=30,
    color="#b576e8",
    name="Grade 4 Gemdraught of Dexterity",
    icon="Grade_4_gemdraught_of_dexterity_icon1.png",
    tags=[SpellTag.UTILITY],
    item=49235,
)
potion_dex.add_specs(NINJA_MAIN, VIPER_MAIN, BARD_MAIN, MACHINIST_MAIN, DANCER_MAIN)


# Grade 4 Gemdraught of Mind
potion_mind = WowPotion(
    spell_id=34603670,
    cooldown=270,
    duration=30,
    color="#b576e8",
    name="Grade 4 Gemdraught of Mind",
    icon="Grade_4_gemdraught_of_mind_icon1.png",
    tags=[SpellTag.UTILITY],
    item=49238,
)
potion_mind.add_specs(WHITE_MAGE_MAIN, SCHOLAR_MAIN, ASTROLOGIAN_MAIN, SAGE_MAIN)


# Grade 4 Gemdraught of Strength
potion_str = WowPotion(
    spell_id=34603666,
    cooldown=270,
    duration=30,
    color="#b576e8",
    name="Grade 4 Gemdraught of Strength",
    icon="Grade_4_gemdraught_of_strength_icon1.png",
    tags=[SpellTag.UTILITY],
    item=49234,
)
potion_str.add_specs(
    PALADIN_MAIN, WARRIOR_MAIN, DARK_KNIGHT_MAIN, GUNBREAKER_MAIN,
    DRAGOON_MAIN, REAPER_MAIN, SAMURAI_MAIN, MONK_MAIN
)


################################################################################
# General Utility
#

sprint = WowSpell(
    spell_id=3,
    cooldown=60,
    duration=10,
    color="#666666",
    name="Sprint",
    icon="Sprint_icon1.png",
    tags=[SpellTag.UTILITY],
)

for spec in ALL_SPECS:
    spec.add_spell(sprint)


################################################################################
# Mana Potions
#


# WowPotion(
#     spell_id=371152,
#     duration=10,
#     color=COL_MANA,
#     name="Potion of Spiritual Clarity",
#     icon="inv_10_alchemy_bottle_shape4_green.jpg",
#     item=191367,
# ).add_specs(*HEAL.specs)
#
# WowPotion(
#     spell_id=371033,
#     duration=10,
#     color=COL_MANA,
#     name="Potion of Frozen Focus",
#     icon="inv_10_alchemy_bottle_shape4_blue.jpg",
#     item=191363,
# ).add_specs(*HEAL.specs)
#
