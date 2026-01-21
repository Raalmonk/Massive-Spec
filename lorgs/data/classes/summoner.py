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
SUMMONER_MAIN.add_spell(spell_id=0, cooldown=0, name="Searing Light", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=0, cooldown=0, name="Summon Bahamut", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=0, cooldown=0, name="Summon Phoenix", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=0, cooldown=0, name="Summon Solar BahaMut", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=0, cooldown=0, name="Summon Ifrit II", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=0, cooldown=0, name="Summon Titan II", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=0, cooldown=0, name="Summon Garuda II", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=0, cooldown=0, name="Necrotize", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SUMMONER_MAIN.add_spell(spell_id=0, cooldown=0, name="Painflare", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
SUMMONER_MAIN.add_spell(spell_id=0, cooldown=0, name="Radiant Aegis", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
SUMMONER_MAIN.add_spell(spell_id=0, cooldown=0, name="Rekindle", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
SUMMONER_MAIN.add_spell(spell_id=0, cooldown=0, name="Addle", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
