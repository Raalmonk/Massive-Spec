"""Define the Summoner Class and its Spec and Spells."""

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
SUMMONER = WowClass(id=27, name="Summoner", color="#2D9B78")

################################################################################
# Specs
#
SUMMONER_MAIN = WowSpec(role=RDPS, wow_class=SUMMONER, name="Summoner")


################################################################################
# Spells
#

# Burst / Cooldowns
SUMMONER_MAIN.add_spell(spell_id=25801, cooldown=120, name="Searing Light", icon="Searing_Light.png", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=7427, cooldown=60, name="Summon Bahamut", icon="Summon_Bahamut.png", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=25831, cooldown=60, name="Summon Phoenix", icon="Summon_Phoenix.png", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=36992, cooldown=60, name="Summon Solar Bahamut", icon="Summon_Solar_Bahamut.png", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=25838, cooldown=2.5, name="Summon Ifrit II", icon="Summon_Ifrit_II.png", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=25839, cooldown=2.5, name="Summon Titan II", icon="Summon_Titan_II.png", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=25840, cooldown=2.5, name="Summon Garuda II", icon="Summon_Garuda_II.png", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=36990, cooldown=1, name="Necrotize", icon="Necrotize.png", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=1295, cooldown=1, name="Painflare", icon="Painflare.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
SUMMONER_MAIN.add_spell(spell_id=25799, cooldown=60, name="Radiant Aegis", icon="Radiant_Aegis.png", tags=[SpellTag.DEFENSIVE])
SUMMONER_MAIN.add_spell(spell_id=12853, cooldown=20, name="Rekindle", icon="Rekindle.png", tags=[SpellTag.DEFENSIVE])
SUMMONER_MAIN.add_spell(spell_id=7560, cooldown=90, name="Addle", icon="Addle.png", tags=[SpellTag.DEFENSIVE])
