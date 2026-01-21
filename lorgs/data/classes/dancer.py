"""Define the Dancer Class and its Spec and Spells."""

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
DANCER = WowClass(id=38, name="Dancer", color="#E2B0AF")

################################################################################
# Specs
#
DANCER_MAIN = WowSpec(role=RDPS, wow_class=DANCER, name="Dancer")


################################################################################
# Spells
#

# Burst / Cooldowns
DANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Standard Step", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
DANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Flourish", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
DANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Technical Step", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
DANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Saber Dance", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
DANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Devilment", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
DANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Second Wind", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
DANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Shield Samba", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
DANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Curing Waltz", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
DANCER_MAIN.add_spell(spell_id=0, cooldown=0, name="Improvisation", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
