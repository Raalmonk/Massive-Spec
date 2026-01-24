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
ASTROLOGIAN_MAIN.add_spell(spell_id=16552, cooldown=120, duration=20, name="Divination", show=True,icon="Divination.png", tags=[SpellTag.DAMAGE])
ASTROLOGIAN_MAIN.add_spell(spell_id=3606, cooldown=60, duration=15, name="Lightspeed", show=True,icon="Lightspeed.png", tags=[SpellTag.DAMAGE])

ASTROLOGIAN_MAIN.add_spell(spell_id=7444, cooldown=1, name="Lord of Crowns", icon="Lord_of_Crowns.png", show=False,tags=[SpellTag.DAMAGE])

# Self Mitigation
ASTROLOGIAN_MAIN.add_spell(spell_id=3614, cooldown=40, name="Essential Dignity", icon="Essential_Dignity.png",show=False, tags=[SpellTag.DEFENSIVE])
ASTROLOGIAN_MAIN.add_spell(spell_id=25873, cooldown=60, duration=8, name="Exaltation", icon="Exaltation.png", show=False,tags=[SpellTag.DEFENSIVE])
ASTROLOGIAN_MAIN.add_spell(spell_id=16556, cooldown=30, name="Celestial Intersection", icon="Celestial_Intersection.png", show=False,tags=[SpellTag.DEFENSIVE])


# Party Mitigation
ASTROLOGIAN_MAIN.add_spell(spell_id=25874, cooldown=180, name="Macrocosmos", icon="Macrocosmos.png",show=True, tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=16559, cooldown=120, duration=30, name="Neutral Sect", show=True,icon="Neutral_Sect.png", tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=7439, cooldown=60, name="Earthly Star", icon="Earthly_Star.png",show=True, tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=3613, cooldown=60, name="Collective Unconscious", icon="Collective_Unconscious.png", show=False,tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=16553, cooldown=60, duration=15, name="Celestial Opposition", icon="Celestial_Opposition.png",show=False, tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=7445, cooldown=1, name="Lady of Crowns", icon="Lady_of_Crowns.png", show=False,tags=[SpellTag.RAID_CD])
ASTROLOGIAN_MAIN.add_spell(spell_id=37031, cooldown=1, duration=15, name="Sun Sign", icon="Sun_Sign.png", show=False,tags=[SpellTag.RAID_CD])
