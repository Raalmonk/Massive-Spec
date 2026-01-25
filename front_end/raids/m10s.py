"""M10S: Red Hot and Deep Blue Timeline."""
from lorgs.models.wow_spell import SpellTag
from .arcadion_heavyweight import RED_HOT_AND_DEEP_BLUE

RED_HOT_AND_DEEP_BLUE.add_cast(
    spell_id="M10S_HOT_IMPACT",
    name="Hot Impact",
    time="0:09", duration=5,
    icon="Hot_Impact.png",
    tags=[SpellTag.TANK_MIT],
    desc="Shared tank buster"
)

RED_HOT_AND_DEEP_BLUE.add_cast(
    spell_id="M10S_PYROTATION",
    name="Pyrotation",
    time="1:04", duration=5,
    icon="Pyrotation.png",
    tags=[SpellTag.RAID_MIT],
    desc="Multi-hit shared damage AoE"
)

RED_HOT_AND_DEEP_BLUE.add_cast(
    spell_id="M10S_DIVERS_DARE_1",
    name="Divers' Dare",
    time="1:18", duration=5,
    icon="Divers_Dare.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage. Clears floor burns"
)

RED_HOT_AND_DEEP_BLUE.add_cast(
    spell_id="M10S_DEEP_IMPACT",
    name="Deep Impact",
    time="2:12", duration=5,
    icon="Deep_Impact.png",
    tags=[SpellTag.TANK_MIT],
    desc="Buster AoE on furthest player"
)

RED_HOT_AND_DEEP_BLUE.add_cast(
    spell_id="M10S_XTREME_SPECTACULAR",
    name="Xtreme Spectacular",
    time="2:37", duration=17, # Including hits
    icon="Xtreme_Spectacular.png",
    tags=[SpellTag.RAID_MIT],
    desc="Proximity damage -> High raid damage"
)

RED_HOT_AND_DEEP_BLUE.add_cast(
    spell_id="M10S_EPIC_BROTHERHOOD",
    name="Epic Brotherhood",
    time="2:59", duration=5,
    icon="Epic_Brotherhood.png",
    tags=[SpellTag.RAID_MIT],
    desc="Equalizes HP between bosses (Raidwide effect)"
)

RED_HOT_AND_DEEP_BLUE.add_cast(
    spell_id="M10S_INSANE_AIR",
    name="Insane Air",
    time="3:09", duration=31, # Sequence
    icon="Insane_Air.png",
    desc="Cone AoEs, Busters, or Shared Cones"
)

RED_HOT_AND_DEEP_BLUE.add_cast(
    spell_id="M10S_DEEP_VARIAL",
    name="Deep Varial",
    time="4:30", duration=7,
    icon="Deep_Varial.png",
    desc="120° cone from wall"
)

RED_HOT_AND_DEEP_BLUE.add_cast(
    spell_id="M10S_HOT_AERIAL",
    name="Hot Aerial",
    time="4:44", duration=7,
    icon="Hot_Aerial.png",
    desc="AoE on furthest player x4"
)

RED_HOT_AND_DEEP_BLUE.add_cast(
    spell_id="M10S_WATERY_GRAVE",
    name="Watery Grave",
    time="5:38", duration=5,
    icon="Watery_Grave.png",
    desc="Binds players"
)

RED_HOT_AND_DEEP_BLUE.add_cast(
    spell_id="M10S_SICKEST_TAKE_OFF",
    name="Sickest Take-off",
    time="7:14", duration=4,
    icon="Sickest_Take-off.png",
    desc="Telegraphs light parties or spreads"
)

RED_HOT_AND_DEEP_BLUE.add_cast(
    spell_id="M10S_DIVERS_DARE_2",
    name="Divers' Dare",
    time="8:44", duration=5,
    icon="Divers_Dare.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage"
)
