"""Define the Monk Class and its Spec and Spells."""

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
MONK = WowClass(id=20, name="Monk", color="#D69C00")

################################################################################
# Specs
#
MONK_MAIN = WowSpec(role=MDPS, wow_class=MONK, name="Monk")


################################################################################
# Spells
#

# Burst / Cooldowns
MONK_MAIN.add_spell(spell_id=0, cooldown=0, name="Perfect Balance", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=0, cooldown=0, name="Riddle of Fire", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=0, cooldown=0, name="Riddle of Wind", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=0, cooldown=0, name="Brotherhood", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
MONK_MAIN.add_spell(spell_id=0, cooldown=0, name="True North", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
MONK_MAIN.add_spell(spell_id=0, cooldown=0, name="Second Wind", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
MONK_MAIN.add_spell(spell_id=0, cooldown=0, name="Bloodbath", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
MONK_MAIN.add_spell(spell_id=0, cooldown=0, name="Riddle of Earth", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
MONK_MAIN.add_spell(spell_id=0, cooldown=0, name="Feint", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
MONK_MAIN.add_spell(spell_id=0, cooldown=0, name="Mantra", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
