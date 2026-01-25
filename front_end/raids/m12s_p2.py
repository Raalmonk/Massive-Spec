"""M12S P2: Lindwurm II Timeline."""
from lorgs.models.wow_spell import SpellTag
from .arcadion_heavyweight import LINDWURM_II

LINDWURM_II.add_cast(
    spell_id="M12S2_ARCADIAN_AFLAME",
    name="Arcadian Aflame",
    time="0:10", duration=5,
    icon="Arcadian_Aflame.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage"
)

LINDWURM_II.add_cast(
    spell_id="M12S2_REPLICATION",
    name="Replication I",
    time="0:25", duration=3,
    icon="Replication.png",
    desc="Creates clones"
)

LINDWURM_II.add_cast(
    spell_id="M12S2_DOUBLE_SOBAT",
    name="Double Sabat", # Typo in CSV is Sobat/Sabat, sticking to CSV name or correction
    time="1:04", duration=6,
    icon="Double_Sobat.png",
    tags=[SpellTag.TANK_MIT],
    desc="Shared damage half room cleave on tank"
)

LINDWURM_II.add_cast(
    spell_id="M12S2_ESOTERIC_FINISHER_1",
    name="Esoteric Finisher",
    time="1:17", duration=5, # Approximate
    icon="Esoteric_Finisher.png",
    tags=[SpellTag.TANK_MIT],
    desc="Buster AoEs on 2 highest enmity"
)

LINDWURM_II.add_cast(
    spell_id="M12S2_FIREFALL_SPLASH",
    name="Firefall Splash",
    time="2:02", duration=6,
    icon="Firefall_Splash.png",
    desc="AoE on player tethered to boss"
)

LINDWURM_II.add_cast(
    spell_id="M12S2_IDYLLIC_DREAM_1",
    name="Idyllic Dream",
    time="4:25", duration=5,
    icon="Idyllic_Dream.png",
    tags=[SpellTag.RAID_MIT],
    desc="High raid damage"
)

LINDWURM_II.add_cast(
    spell_id="M12S2_LINDWURMS_METEOR",
    name="Lindwurm's Meteor",
    time="5:44", duration=5, # Approximate
    icon="Lindwurms_Meteor.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage. Changes platform shape"
)

LINDWURM_II.add_cast(
    spell_id="M12S2_ARCADIAN_ARCANUM",
    name="Arcadian Arcanum",
    time="5:53", duration=4,
    icon="Arcadian_Arcanum.png",
    desc="Spread AoEs on 4 players"
)

LINDWURM_II.add_cast(
    spell_id="M12S2_ESOTERIC_FINISHER_2",
    name="Esoteric Finisher",
    time="8:08", duration=5, # Approximate
    icon="Esoteric_Finisher.png",
    tags=[SpellTag.TANK_MIT],
    desc="Buster AoEs"
)

LINDWURM_II.add_cast(
    spell_id="M12S2_ARCADIAN_HELL",
    name="Arcadian Hell",
    time="8:30", duration=5,
    icon="Arcadian_Hell.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage from all clones"
)
