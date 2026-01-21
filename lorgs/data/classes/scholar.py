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
SCHOLAR_MAIN.add_spell(spell_id=166, cooldown=60, name="Aetherflow", icon="Aetherflow.png", tags=[SpellTag.DAMAGE])
SCHOLAR_MAIN.add_spell(spell_id=7436, cooldown=120, name="Chain Stratagem", icon="Chain_Stratagem.png", tags=[SpellTag.DAMAGE])
SCHOLAR_MAIN.add_spell(spell_id=3587, cooldown=180, name="Dissipation", icon="Dissipation.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
SCHOLAR_MAIN.add_spell(spell_id=7434, cooldown=45, name="Excogitation", icon="Excogitation.png", tags=[SpellTag.DEFENSIVE])
SCHOLAR_MAIN.add_spell(spell_id=7423, cooldown=3, name="Aetherpact", icon="Aetherpact.png", tags=[SpellTag.DEFENSIVE])
SCHOLAR_MAIN.add_spell(spell_id=189, cooldown=1, name="Lustrate", icon="Lustrate.png", tags=[SpellTag.DEFENSIVE])
SCHOLAR_MAIN.add_spell(spell_id=16542, cooldown=60, name="Recitation", icon="Recitation.png", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
SCHOLAR_MAIN.add_spell(spell_id=188, cooldown=30, name="Sacred Soil", icon="Sacred_Soil.png", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=3583, cooldown=30, name="Indomitability", icon="Indomitability.png", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=3585, cooldown=90, name="Deployment Tactics", icon="Deployment_Tactics.png", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=16543, cooldown=60, name="Fey Blessing", icon="Fey_Blessing.png", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=16545, cooldown=120, name="Summon Seraph", icon="Summon_Seraph.png", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=16546, cooldown=20, name="Consolation", icon="Consolation.png", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=25868, cooldown=120, name="Expedient", icon="Expedient.png", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=37014, cooldown=180, name="Seraphism", icon="Seraphism.png", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=805, cooldown=0, name="Fey Illumination", icon="Fey_Illumination.png", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=37013, cooldown=2.5, name="Concitation", icon="Concitation.png", tags=[SpellTag.RAID_CD])
SCHOLAR_MAIN.add_spell(spell_id=37016, cooldown=2.5, name="Accession", icon="Accession.png", tags=[SpellTag.RAID_CD])
