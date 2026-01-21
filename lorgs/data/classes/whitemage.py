"""Define the White Mage Class and its Spec and Spells."""

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
WHITE_MAGE = WowClass(id=24, name="White Mage", color="#FFF0F5")

################################################################################
# Specs
#
WHITE_MAGE_MAIN = WowSpec(role=HEAL, wow_class=WHITE_MAGE, name="White Mage")


################################################################################
# Spells
#

# Burst / Cooldowns
WHITE_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Presence of Mind", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
WHITE_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Afflatus Misery", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
WHITE_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Tetragrammaton", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
WHITE_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Aquaveil", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
WHITE_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Divine Benison", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
WHITE_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Liturgy of the Bell", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
WHITE_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Temperance", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Plenary Indulgence", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Divine Caress", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Assize", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
