"""Define the Scholar Class and its Spec and Spells."""

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
SCHOLAR = WowClass(id=28, name="Scholar", color="#8657FF")

################################################################################
# Specs
#
SCHOLAR_MAIN = WowSpec(role=HEAL, wow_class=SCHOLAR, name="Scholar")


################################################################################
# Spells
#

# Burst / Cooldowns
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Aetherflow", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Chain Stratagem", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Dissipation", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Excogitation", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Aetherpact", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Lustrate", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Recitation", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Sacred Soil", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Indomitability", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Deployment Tactics", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Fey Blessing", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Summon Seraph", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Consolation", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Expedient", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Seraphism", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Fey Illumination", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Concitation", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=0, cooldown=0, name="Accession", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
