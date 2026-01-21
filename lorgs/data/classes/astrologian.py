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
ASTROLOGIAN_MAIN.add_spell(spell_id=0, cooldown=0, name="Lightspeed", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
ASTROLOGIAN_MAIN.add_spell(spell_id=0, cooldown=0, name="Divination", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
ASTROLOGIAN_MAIN.add_spell(spell_id=0, cooldown=0, name="Lord of Crowns", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
ASTROLOGIAN_MAIN.add_spell(spell_id=0, cooldown=0, name="Essential Dignity", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
ASTROLOGIAN_MAIN.add_spell(spell_id=0, cooldown=0, name="Exaltation", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
ASTROLOGIAN_MAIN.add_spell(spell_id=0, cooldown=0, name="Celestial Intersection", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
ASTROLOGIAN_MAIN.add_spell(spell_id=0, cooldown=0, name="Macrocosmos", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
ASTROLOGIAN_MAIN.add_spell(spell_id=0, cooldown=0, name="Neutral Sect", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=0, cooldown=0, name="Collective Unconscious", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=0, cooldown=0, name="Celestial Opposition", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=0, cooldown=0, name="Lady of Crowns", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=0, cooldown=0, name="Sun Sign", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=0, cooldown=0, name="Earthly Star", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
