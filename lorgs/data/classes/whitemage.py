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
WHITE_MAGE_MAIN.add_spell(spell_id=136, cooldown=120, name="Presence of Mind", icon="Presence_of_Mind.png", tags=[SpellTag.DAMAGE])
WHITE_MAGE_MAIN.add_spell(spell_id=16535, cooldown=2.5, name="Afflatus Misery", icon="Afflatus_Misery.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
WHITE_MAGE_MAIN.add_spell(spell_id=3570, cooldown=60, name="Tetragrammaton", icon="Tetragrammaton.png", tags=[SpellTag.DEFENSIVE])
WHITE_MAGE_MAIN.add_spell(spell_id=25861, cooldown=60, name="Aquaveil", icon="Aquaveil.png", tags=[SpellTag.DEFENSIVE])
WHITE_MAGE_MAIN.add_spell(spell_id=7432, cooldown=30, name="Divine Benison", icon="Divine_Benison.png", tags=[SpellTag.DEFENSIVE])
WHITE_MAGE_MAIN.add_spell(spell_id=25862, cooldown=180, name="Liturgy of the Bell", icon="Liturgy_of_the_Bell.png", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
WHITE_MAGE_MAIN.add_spell(spell_id=16536, cooldown=120, name="Temperance", icon="Temperance.png", tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=7433, cooldown=60, name="Plenary Indulgence", icon="Plenary_Indulgence.png", tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=37011, cooldown=1, name="Divine Caress", icon="Divine_Caress.png", tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=3571, cooldown=40, name="Assize", icon="Assize.png", tags=[SpellTag.RAID_CD])
