"""Define the Reaper Class and its Spec and Spells."""

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
REAPER = WowClass(id=39, name="Reaper", color="#965A90")

################################################################################
# Specs
#
REAPER_MAIN = WowSpec(role=MDPS, wow_class=REAPER, name="Reaper")


################################################################################
# Spells
#

# Burst / Cooldowns
REAPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Soul Slice", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
REAPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Gluttony", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
REAPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Enshroud", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
REAPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Arcane Circle", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
REAPER_MAIN.add_spell(spell_id=0, cooldown=0, name="True North", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
REAPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Second Wind", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
REAPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Bloodbath", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
REAPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Feint", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
REAPER_MAIN.add_spell(spell_id=0, cooldown=0, name="Arcane Crest", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
