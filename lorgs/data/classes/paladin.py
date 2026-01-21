"""Define the Paladin Class and its Spec and Spells."""

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
PALADIN = WowClass(id=19, name="Paladin", color="#A8D2E6")

################################################################################
# Specs
#
PALADIN_MAIN = WowSpec(role=TANK, wow_class=PALADIN, name="Paladin")


################################################################################
# Spells
#

# Burst / Cooldowns
PALADIN_MAIN.add_spell(spell_id=0, cooldown=0, name="Fight or Flight", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
PALADIN_MAIN.add_spell(spell_id=0, cooldown=0, name="Guardian", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
PALADIN_MAIN.add_spell(spell_id=0, cooldown=0, name="Bulwark", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
PALADIN_MAIN.add_spell(spell_id=0, cooldown=0, name="Rampart", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
PALADIN_MAIN.add_spell(spell_id=0, cooldown=0, name="Holy Sheltron", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
PALADIN_MAIN.add_spell(spell_id=0, cooldown=0, name="Intervention", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
PALADIN_MAIN.add_spell(spell_id=0, cooldown=0, name="Cover", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
PALADIN_MAIN.add_spell(spell_id=0, cooldown=0, name="Hallowed Ground", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
PALADIN_MAIN.add_spell(spell_id=0, cooldown=0, name="Reprisal", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
PALADIN_MAIN.add_spell(spell_id=0, cooldown=0, name="Divine Veil", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
PALADIN_MAIN.add_spell(spell_id=0, cooldown=0, name="Passage of Arms", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
