"""Define the Dragoon Class and its Spec and Spells."""

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
DRAGOON = WowClass(id=22, name="Dragoon", color="#4164CD")

################################################################################
# Specs
#
DRAGOON_MAIN = WowSpec(role=MDPS, wow_class=DRAGOON, name="Dragoon")


################################################################################
# Spells
#

# Burst / Cooldowns
DRAGOON_MAIN.add_spell(spell_id=0, cooldown=0, name="High Jump", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
DRAGOON_MAIN.add_spell(spell_id=0, cooldown=0, name="Geirskougul", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
DRAGOON_MAIN.add_spell(spell_id=0, cooldown=0, name="Lance Charge", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
DRAGOON_MAIN.add_spell(spell_id=0, cooldown=0, name="Battle Litany", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])
DRAGOON_MAIN.add_spell(spell_id=0, cooldown=0, name="True North", icon="placeholder.jpg", tags=[SpellTag.DAMAGE])

# Self Mitigation
DRAGOON_MAIN.add_spell(spell_id=0, cooldown=0, name="Second Wind", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
DRAGOON_MAIN.add_spell(spell_id=0, cooldown=0, name="Bloodbath", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
DRAGOON_MAIN.add_spell(spell_id=0, cooldown=0, name="Feint", icon="placeholder.jpg", tags=[SpellTag.DEFENSIVE])
