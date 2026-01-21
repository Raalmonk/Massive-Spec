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
BLACK_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Transpose", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Flare", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Flare Star", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Xenoglossy", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Foul", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Ley Lines", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Triplecast", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Swiftcast", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Manafont", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
BLACK_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Paradox", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
BLACK_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Manaward", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
BLACK_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Addle", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
