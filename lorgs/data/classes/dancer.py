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
DANCER_MAIN.add_spell(spell_id=15997, cooldown=30, name="Standard Step", icon="Standard_Step.png", tags=[SpellTag.DAMAGE])
DANCER_MAIN.add_spell(spell_id=16013, cooldown=60, name="Flourish", icon="Flourish.png", tags=[SpellTag.DAMAGE])
DANCER_MAIN.add_spell(spell_id=15998, cooldown=120, name="Technical Step", icon="Technical_Step.png", tags=[SpellTag.DAMAGE])
DANCER_MAIN.add_spell(spell_id=16005, cooldown=2.5, name="Saber Dance", icon="Saber_Dance.png", tags=[SpellTag.DAMAGE])
DANCER_MAIN.add_spell(spell_id=16011, cooldown=120, name="Devilment", icon="Devilment.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
DANCER_MAIN.add_spell(spell_id=57, cooldown=120, name="Second Wind", icon="Second_Wind.png", tags=[SpellTag.DEFENSIVE])
DANCER_MAIN.add_spell(spell_id=16012, cooldown=90, name="Shield Samba", icon="Shield_Samba.png", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
DANCER_MAIN.add_spell(spell_id=16015, cooldown=60, name="Curing Waltz", icon="Curing_Waltz.png", tags=[SpellTag.RAID_CD])
DANCER_MAIN.add_spell(spell_id=16014, cooldown=120, name="Improvisation", icon="Improvisation.png", tags=[SpellTag.RAID_CD])
