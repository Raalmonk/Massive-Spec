"""Define the Sage Class and its Spec and Spells."""

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
SAGE = WowClass(id=40, name="Sage", color="#80A0F0")

################################################################################
# Specs
#
SAGE_MAIN = WowSpec(role=HEAL, wow_class=SAGE, name="Sage")


################################################################################
# Spells
#

# Burst / Cooldowns
SAGE_MAIN.add_spell(spell_id=38927, cooldown=2, name="Psyche", icon="Psyche.png", tags=[SpellTag.DAMAGE])
SAGE_MAIN.add_spell(spell_id=37407, cooldown=2, name="Phlegma III", icon="Phlegma_III.png", tags=[SpellTag.DAMAGE])

# Self Mitigation
SAGE_MAIN.add_spell(spell_id=38911, cooldown=45, name="Taurochole", icon="Taurochole.png", tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=38918, cooldown=120, name="Haima", icon="Haima.png", tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=38924, cooldown=1, name="Druochole", icon="Druochole.png", tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=24294, cooldown=60, name="Soteria", icon="Soteria.png", tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=24317, cooldown=60, name="Krasis", icon="Krasis.png", tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=24300, cooldown=90, name="Zoe", icon="Zoe.png", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
SAGE_MAIN.add_spell(spell_id=38923, cooldown=30, name="Kerachole", icon="Kerachole.png", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=38915, cooldown=30, name="Ixochole", icon="Ixochole.png", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=38925, cooldown=120, name="Holos", icon="Holos.png", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=38919, cooldown=60, name="Physis II", icon="Physis_II.png", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=38926, cooldown=120, name="Panhaima", icon="Panhaima.png", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=27830, cooldown=45, name="Pneuma", icon="Pneuma.png", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=37035, cooldown=180, name="Philosophia", icon="Philosophia.png", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=38916, cooldown=2, name="Eukrasian Prognosis II", icon="Eukrasian_Prognosis_II.png", tags=[SpellTag.RAID_CD])
