"""M11S: The Tyrant Timeline."""
from lorgs.models.wow_spell import SpellTag
from .arcadion_heavyweight import THE_TYRANT

THE_TYRANT.add_cast(
    spell_id="M11S_CROWN_OF_ARCADIA_1",
    name="Crown of Arcadia",
    time="0:05", duration=5,
    icon="Crown_of_Arcadia.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage"
)

THE_TYRANT.add_cast(
    spell_id="M11S_RAW_STEEL_1",
    name="Raw Steel",
    time="0:25", duration=5, # Estimated cast/hit
    icon="Raw_Steel.png",
    tags=[SpellTag.TANK_MIT],
    desc="Shared buster on tanks or Spread AoEs"
)

THE_TYRANT.add_cast(
    spell_id="M11S_ASSAULT_EVOLVED",
    name="Assault Evolved",
    time="0:41", duration=20, # Sequence
    icon="Assault_Evolved.png",
    desc="Boss weapon abilities sequence"
)

THE_TYRANT.add_cast(
    spell_id="M11S_VOID_STARDUST",
    name="Void Stardust",
    time="1:15", duration=14,
    icon="Void_Stardust.png",
    desc="Baited circles + Stack/Spread"
)

THE_TYRANT.add_cast(
    spell_id="M11S_CROWN_OF_ARCADIA_2",
    name="Crown of Arcadia",
    time="1:57", duration=5,
    icon="Crown_of_Arcadia.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage"
)

THE_TYRANT.add_cast(
    spell_id="M11S_ONE_AND_ONLY",
    name="One and Only",
    time="3:52", duration=9,
    icon="One_and_Only.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage"
)

THE_TYRANT.add_cast(
    spell_id="M11S_GREAT_WALL_OF_FIRE",
    name="Great Wall of Fire",
    time="4:08", duration=5,
    icon="Great_Wall_of_Fire.png",
    tags=[SpellTag.TANK_MIT],
    desc="Shared damage line buster"
)

THE_TYRANT.add_cast(
    spell_id="M11S_FIRE_AND_FURY",
    name="Fire and Fury",
    time="4:31", duration=5,
    icon="Fire_and_Fury.png",
    desc="Cone AoEs + Portal Lines"
)

THE_TYRANT.add_cast(
    spell_id="M11S_TRIPLE_TYRANNIHILATION",
    name="Triple Tyrannihilation",
    time="5:36", duration=7,
    icon="Triple_Tyrannihilation.png",
    tags=[SpellTag.RAID_MIT],
    desc="3-hit extreme raid damage"
)

THE_TYRANT.add_cast(
    spell_id="M11S_MAJESTIC_METEOR",
    name="Majestic Meteor",
    time="6:12", duration=5,
    icon="Majestic_Meteor.png",
    desc="Mechanic set start"
)

THE_TYRANT.add_cast(
    spell_id="M11S_MASSIVE_METEOR",
    name="Massive Meteor",
    time="7:21", duration=6,
    icon="Massive_Meteor.png",
    tags=[SpellTag.RAID_MIT],
    desc="5-hit shared damage AoE on healers"
)

THE_TYRANT.add_cast(
    spell_id="M11S_ARCADIAN_AVALANCHE",
    name="Arcadian Avalanche",
    time="7:35", duration=16,
    icon="Arcadian_Avalanche.png",
    desc="Platform slam line AoE"
)

THE_TYRANT.add_cast(
    spell_id="M11S_ECLIPTIC_STAMPEDE",
    name="Ecliptic Stampede",
    time="8:51", duration=5,
    icon="Ecliptic_Stampede.png",
    tags=[SpellTag.RAID_MIT],
    desc="Mechanic set (Raid Damage)"
)
