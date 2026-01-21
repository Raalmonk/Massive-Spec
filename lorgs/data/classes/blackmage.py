"""Define the Black Mage Class and its Spec and Spells."""

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
BLACK_MAGE = WowClass(id=25, name="Black Mage", color="#A579D6")

################################################################################
# Specs
#
BLACK_MAGE_MAIN = WowSpec(role=RDPS, wow_class=BLACK_MAGE, name="Black Mage")


################################################################################
# Spells
#

# Burst / Cooldowns
BLACK_MAGE_MAIN.add_spell(spell_id=149, cooldown=5, name="Transpose", icon="Transpose.png", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=162, cooldown=2.5, name="Flare", icon="Flare.png", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=3003, cooldown=0, name="Flare Star", icon="Flare_Star.png", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=16507, cooldown=2.5, name="Xenoglossy", icon="Xenoglossy.png", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=7422, cooldown=2.5, name="Foul", icon="Foul.png", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=3573, cooldown=120, name="Ley Lines", icon="Ley_Lines.png", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=7421, cooldown=60, name="Triplecast", icon="Triplecast.png", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=150, cooldown=40, name="Swiftcast", icon="Swiftcast.png", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=158, cooldown=100, name="Manafont", icon="Manafont.png", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=4325, cooldown=0, name="Paradox", icon="Paradox.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
BLACK_MAGE_MAIN.add_spell(spell_id=157, cooldown=120, name="Manaward", icon="Manaward.png", tags=[SpellTag.DEFENSIVE])
BLACK_MAGE_MAIN.add_spell(spell_id=7560, cooldown=90, name="Addle", icon="Addle.png", tags=[SpellTag.DEFENSIVE])
