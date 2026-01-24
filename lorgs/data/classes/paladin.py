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
PALADIN_MAIN.add_spell(spell_id=20, cooldown=60, duration=20, show=True, name="Fight or Flight", icon="Fight_or_Flight.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
PALADIN_MAIN.add_spell(spell_id=36920, cooldown=120, duration=15, show=True, name="Guardian", icon="Guardian.png", tags=[SpellTag.DEFENSIVE])
PALADIN_MAIN.add_spell(spell_id=7531, cooldown=90, duration=20, show=True, name="Rampart", icon="Rampart.png", tags=[SpellTag.DEFENSIVE])
PALADIN_MAIN.add_spell(spell_id=22, cooldown=90, duration=10, show=True, name="Bulwark", icon="Bulwark.png", tags=[SpellTag.DEFENSIVE])
PALADIN_MAIN.add_spell(spell_id=25746, cooldown=5, duration=4, show=False, name="Holy Sheltron", icon="Holy_Sheltron.png", tags=[SpellTag.DEFENSIVE])
PALADIN_MAIN.add_spell(spell_id=7382, cooldown=10, duration=4, show=False, name="Intervention", icon="Intervention.png", tags=[SpellTag.DEFENSIVE])
PALADIN_MAIN.add_spell(spell_id=30, cooldown=420, duration=10, show=True, name="Hallowed Ground", icon="Hallowed_Ground.png", tags=[SpellTag.DEFENSIVE])
PALADIN_MAIN.add_spell(spell_id=27, cooldown=120, name="Cover",show=False,  icon="Cover.png", tags=[SpellTag.DEFENSIVE])


# Party Mitigation
PALADIN_MAIN.add_spell(spell_id=7535, cooldown=60, duration=15, show=True, name="Reprisal", icon="Reprisal.png", tags=[SpellTag.RAID_CD])
PALADIN_MAIN.add_spell(spell_id=3540, cooldown=90, name="Divine Veil", icon="Divine_Veil.png", tags=[SpellTag.RAID_CD])
PALADIN_MAIN.add_spell(spell_id=7385, cooldown=120, name="Passage of Arms", icon="Passage_of_Arms.png", tags=[SpellTag.RAID_CD])
