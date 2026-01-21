"""Define the Red Mage Class and its Spec and Spells."""

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
RED_MAGE = WowClass(id=35, name="Red Mage", color="#E87B7B")

################################################################################
# Specs
#
RED_MAGE_MAIN = WowSpec(role=RDPS, wow_class=RED_MAGE, name="Red Mage")


################################################################################
# Spells
#

# Burst / Cooldowns
RED_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Embolden", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Fleche", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Contre Sixte", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Manafication", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Acceleration", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Embloden", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Enchanted Riposte", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Swiftcast", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Enchanted Reprise", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
RED_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Vercure", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
RED_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Addle", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
RED_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Magick Barrier", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
