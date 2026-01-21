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
RED_MAGE_MAIN.add_spell(spell_id=7520, cooldown=120, name="Embolden", icon="Embolden.png", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=7517, cooldown=25, name="Fleche", icon="Fleche.png", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=7519, cooldown=35, name="Contre Sixte", icon="Contre_Sixte.png", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=7521, cooldown=110, name="Manafication", icon="Manafication.png", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=7518, cooldown=55, name="Acceleration", icon="Acceleration.png", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=7520, cooldown=120, name="Embolden", icon="Embolden.png", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=7527, cooldown=1.5, name="Enchanted Riposte", icon="Enchanted_Riposte.png", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=150, cooldown=40, name="Swiftcast", icon="Swiftcast.png", tags=[SpellTag.DAMAGE])
RED_MAGE_MAIN.add_spell(spell_id=16528, cooldown=2.5, name="Enchanted Reprise", icon="Enchanted_Reprise.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
RED_MAGE_MAIN.add_spell(spell_id=7514, cooldown=2.5, name="Vercure", icon="Vercure.png", tags=[SpellTag.DEFENSIVE])
RED_MAGE_MAIN.add_spell(spell_id=7560, cooldown=90, name="Addle", icon="Addle.png", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
RED_MAGE_MAIN.add_spell(spell_id=25857, cooldown=120, name="Magick Barrier", icon="Magick_Barrier.png", tags=[SpellTag.RAID_CD])
