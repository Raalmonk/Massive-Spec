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
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Psyche", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Phlegma III", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Taurochole", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Haima", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Druochole", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Soteria", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Krasis", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Zoe", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])

# Party Mitigation
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Kerachole", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Ixochole", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Holos", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Physis II", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Panhaima", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Pneuma", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Philosophia", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=0, cooldown=0, name="Eukrasian Prognosis II", icon="placeholder.jpg", tags=[SpellTag.RAID_CD])
