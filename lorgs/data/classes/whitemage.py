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
WHITE_MAGE_MAIN.add_spell(spell_id=136, cooldown=120, duration=15, name="Presence of Mind", show=True,icon="Presence_of_Mind.png", tags=[SpellTag.DAMAGE])
WHITE_MAGE_MAIN.add_spell(spell_id=16535, cooldown=2.5, name="Afflatus Misery", show=True,icon="Afflatus_Misery.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
WHITE_MAGE_MAIN.add_spell(spell_id=3570, cooldown=60, name="Tetragrammaton", show=False,icon="Tetragrammaton.png", tags=[SpellTag.DEFENSIVE])
WHITE_MAGE_MAIN.add_spell(spell_id=25861, cooldown=60, duration=8, name="Aquaveil", show=False,icon="Aquaveil.png", tags=[SpellTag.DEFENSIVE])
WHITE_MAGE_MAIN.add_spell(spell_id=7432, cooldown=30, name="Divine Benison", show=False,icon="Divine_Benison.png", tags=[SpellTag.DEFENSIVE])
WHITE_MAGE_MAIN.add_spell(spell_id=16531, cooldown=0, name="Afflatus_Solace", show=False,icon="Afflatus_Solace.png", tags=[SpellTag.DEFENSIVE])
WHITE_MAGE_MAIN.add_spell(spell_id=135, cooldown=0, name="Cure II", show=False,icon="Cure_II.png", tags=[SpellTag.DEFENSIVE])
WHITE_MAGE_MAIN.add_spell(spell_id=1000158, cooldown=0, name="Regen", duration = 18,show=False,icon="Regen.png", tags=[SpellTag.DEFENSIVE])
# Party Mitigation
WHITE_MAGE_MAIN.add_spell(spell_id=25862, cooldown=180,  name="Liturgy of the Bell", show=True,icon="Liturgy_of_the_Bell.png", tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=16536, cooldown=120, duration=20, name="Temperance", show=True,icon="Temperance.png", tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=7433, cooldown=60, duration=10, name="Plenary Indulgence", show=True,icon="Plenary_Indulgence.png", tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=37011, cooldown=1, name="Divine Caress", show=False,icon="Divine_Caress.png", tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=3571, cooldown=40, name="Assize", icon="Assize.png", show=False,tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=16534, cooldown=0, name="Afflatus_Rapture", show=False,icon="Afflatus_Rapture.png", tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=131, cooldown=0, name="Cure III", show=False,icon="Cure_III.png", tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=37010, cooldown=0, name="Medica III",duration = 15 ,show=False,icon="Medica_III.png", tags=[SpellTag.RAID_CD])
WHITE_MAGE_MAIN.add_spell(spell_id=124, cooldown=0, name="Medica", show=False,icon="Medica.png", tags=[SpellTag.RAID_CD])