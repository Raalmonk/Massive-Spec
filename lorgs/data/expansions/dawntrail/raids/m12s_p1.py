"""M12S P1: Lindwurm Timeline."""
from lorgs.models.wow_spell import SpellTag
from .arcadion_heavyweight import LINDWURM

LINDWURM.add_cast(
    spell_id="M12S1_THE_FIXER_1",
    name="The Fixer",
    time="0:10", duration=5,
    icon="The_Fixer.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage"
)

LINDWURM.add_cast(
    spell_id="M12S1_MORTAL_SLAYER",
    name="Mortal Slayer",
    time="0:29", duration=12,
    icon="Mortal_Slayer.png",
    desc="Orbs on wing. Purple = Busters"
)

LINDWURM.add_cast(
    spell_id="M12S1_VISCERAL_BURST",
    name="Visceral Burst",
    time="1:37", duration=5, # Approximate from sequence
    icon="Visceral_Burst.png",
    tags=[SpellTag.TANK_MIT],
    desc="Tank busters on both tanks"
)

LINDWURM.add_cast(
    spell_id="M12S1_CRUEL_COIL",
    name="Cruel Coil",
    time="2:12", duration=3,
    icon="Cruel_Coil.png",
    desc="Draws players to middle"
)

LINDWURM.add_cast(
    spell_id="M12S1_SKINSPLITTER",
    name="Skinsplitter",
    time="2:21", duration=5,
    icon="Skinsplitter.png",
    desc="Boss rotates, changing opening"
)

LINDWURM.add_cast(
    spell_id="M12S1_SPLATTERSHED_1",
    name="Splattershed",
    time="3:03", duration=5,
    icon="Splattershed.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage. Boss grows new arms"
)

LINDWURM.add_cast(
    spell_id="M12S1_BRING_DOWN_THE_HOUSE",
    name="Bring Down the House",
    time="3:36", duration=5, # Approximate
    icon="Bring_Down_the_House.png",
    desc="Destroys segments of the arena"
)

LINDWURM.add_cast(
    spell_id="M12S1_SPLIT_SCOURGE",
    name="Split Scourge",
    time="3:49", duration=5, # Approximate
    icon="Split_Scourge.png",
    tags=[SpellTag.TANK_MIT],
    desc="Line tank buster"
)

LINDWURM.add_cast(
    spell_id="M12S1_SPLATTERSHED_2",
    name="Splattershed",
    time="4:44", duration=6,
    icon="Splattershed.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage"
)

LINDWURM.add_cast(
    spell_id="M12S1_SLAUGHTERSHED",
    name="Slaughtershed",
    time="5:37", duration=3,
    icon="Slaughtershed.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage"
)

LINDWURM.add_cast(
    spell_id="M12S1_REFRESHING_OVERKILL",
    name="Refreshing Overkill",
    time="7:08", duration=10,
    icon="Refreshing_Overkill.png",
    tags=[SpellTag.RAID_MIT],
    desc="Enrage sequence"
)
