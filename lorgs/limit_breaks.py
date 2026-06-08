"""FF14 PvE Limit Break actions shared by every job."""

from __future__ import annotations

from lorgs.models.wow_spell import SpellTag
from lorgs.models.wow_spell import WowSpell


LIMIT_BREAKS = [
    WowSpell(spell_id=197, name="Shield Wall", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=198, name="Stronghold", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=199, name="Last Bastion", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=200, name="Braver", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=201, name="Bladedance", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=202, name="Final Heaven", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=203, name="Skyshard", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=204, name="Starstorm", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=205, name="Meteor", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=206, name="Healing Wind", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=207, name="Breath of the Earth", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=208, name="Pulse of Life", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=4238, name="Big Shot", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=4239, name="Desperado", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=4240, name="Land Waker", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=4241, name="Dark Force", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=4242, name="Dragonsong Dive", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=4243, name="Chimatsuri", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=4244, name="Sagittarius Arrow", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=4245, name="Satellite Beam", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=4246, name="Teraflare", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=4247, name="Angel Feathers", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=4248, name="Astral Stasis", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=7861, name="Doom of the Living", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=7862, name="Vermilion Scourge", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=17105, name="Gunmetal Soul", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=17106, name="Crimson Lotus", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=24858, name="The End", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=24859, name="Techne Makre", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=34866, name="World-swallower", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
    WowSpell(spell_id=34867, name="Chromatic Fantasy", icon="Limit_Break.png", show=True, tags=[SpellTag.UTILITY]),
]

LIMIT_BREAK_SPELL_BY_ID = {spell.spell_id: spell for spell in LIMIT_BREAKS}
LIMIT_BREAK_SPELL_IDS = set(LIMIT_BREAK_SPELL_BY_ID)


def is_limit_break_spell_id(spell_id: int) -> bool:
    return spell_id in LIMIT_BREAK_SPELL_IDS
