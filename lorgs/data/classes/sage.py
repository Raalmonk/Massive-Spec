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
SAGE_MAIN.add_spell(spell_id=37033, cooldown=60, name="Psyche", icon="Psyche.png",show=False, tags=[SpellTag.DAMAGE])
SAGE_MAIN.add_spell(spell_id=24313, cooldown=40, name="Phlegma III", icon="Phlegma_III.png", show=False,tags=[SpellTag.DAMAGE])
SAGE_MAIN.add_spell(spell_id=24300, cooldown=90, duration=30, name="Zoe", icon="Zoe.png", show=False,tags=[SpellTag.DAMAGE])
# Self Mitigation
SAGE_MAIN.add_spell(spell_id=24303, cooldown=45, duration=15, name="Taurochole", icon="Taurochole.png",show=False, tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=24305, cooldown=120, duration=15, name="Haima", icon="Haima.png",show=False, tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=24296, cooldown=1, name="Druochole", icon="Druochole.png", show=False,tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=24294, cooldown=60, duration=15, name="Soteria", icon="Soteria.png", show=False,tags=[SpellTag.DEFENSIVE])
SAGE_MAIN.add_spell(spell_id=24317, cooldown=60, duration=10, name="Krasis", icon="Krasis.png",show=False, tags=[SpellTag.DEFENSIVE])


# Party Mitigation
SAGE_MAIN.add_spell(spell_id=37035, cooldown=180, duration=20, name="Philosophia", show=True,icon="Philosophia.png", tags=[SpellTag.RAID_CD])


SAGE_MAIN.add_spell(spell_id=24310, cooldown=120, duration=20, name="Holos", show=True,icon="Holos.png", tags=[SpellTag.RAID_CD])

SAGE_MAIN.add_spell(spell_id=24311, cooldown=120, duration=15, name="Panhaima", show=True,icon="Panhaima.png", tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=24318, cooldown=120, name="Pneuma", icon="Pneuma.png", show=True,tags=[SpellTag.RAID_CD])

SAGE_MAIN.add_spell(spell_id=24298, cooldown=30, duration=15, name="Kerachole", icon="Kerachole.png",show=False, tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=24299, cooldown=30, name="Ixochole", icon="Ixochole.png",show=False, tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=24302, cooldown=60, duration=15, name="Physis II", icon="Physis_II.png",show=False, tags=[SpellTag.RAID_CD])
SAGE_MAIN.add_spell(spell_id=37034, cooldown=1.5, name="Eukrasian Prognosis II", icon="Eukrasian_Prognosis_II.png", show=False,tags=[SpellTag.RAID_CD])