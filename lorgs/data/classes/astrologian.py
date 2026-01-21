"""Define the Astrologian Class and its Spec and Spells."""

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
ASTROLOGIAN = WowClass(id=33, name="Astrologian", color="#FFE74A")

################################################################################
# Specs
#
ASTROLOGIAN_MAIN = WowSpec(role=HEAL, wow_class=ASTROLOGIAN, name="Astrologian")


################################################################################
# Spells
#

# Burst / Cooldowns
ASTROLOGIAN_MAIN.add_spell(spell_id=8917, cooldown=60, name="Lightspeed", icon="Lightspeed.png", tags=[SpellTag.DAMAGE])
ASTROLOGIAN_MAIN.add_spell(spell_id=18941, cooldown=120, name="Divination", icon="Divination.png", tags=[SpellTag.DAMAGE])
ASTROLOGIAN_MAIN.add_spell(spell_id=38901, cooldown=1, name="Lord of Crowns", icon="Lord_of_Crowns.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
ASTROLOGIAN_MAIN.add_spell(spell_id=38906, cooldown=40, name="Essential Dignity", icon="Essential_Dignity.png", tags=[SpellTag.DEFENSIVE])
ASTROLOGIAN_MAIN.add_spell(spell_id=38888, cooldown=60, name="Exaltation", icon="Exaltation.png", tags=[SpellTag.DEFENSIVE])
ASTROLOGIAN_MAIN.add_spell(spell_id=38908, cooldown=30, name="Celestial Intersection", icon="Celestial_Intersection.png", tags=[SpellTag.DEFENSIVE])
ASTROLOGIAN_MAIN.add_spell(spell_id=38903, cooldown=60, name="Macrocosmos", icon="Macrocosmos.png", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
ASTROLOGIAN_MAIN.add_spell(spell_id=38886, cooldown=120, name="Neutral Sect", icon="Neutral_Sect.png", tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=3613, cooldown=60, name="Collective Unconscious", icon="Collective_Unconscious.png", tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=38907, cooldown=60, name="Celestial Opposition", icon="Celestial_Opposition.png", tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=38902, cooldown=1, name="Lady of Crowns", icon="Lady_of_Crowns.png", tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=38887, cooldown=1, name="Sun Sign", icon="Sun_Sign.png", tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=7439, cooldown=60, name="Earthly Star", icon="Earthly_Star.png", tags=[SpellTag.RAID_CD])
