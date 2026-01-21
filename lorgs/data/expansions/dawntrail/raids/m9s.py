"""M9S: Vamp Fatale Timeline."""
from lorgs.models.wow_spell import SpellTag
from .arcadion_heavyweight import VAMP_FATALE

# --- Timeline (String IDs + Descriptions) ---

VAMP_FATALE.add_cast(
    spell_id="M9S_KILLER_VOICE",
    name="Killer Voice",
    time="0:05", duration=5,
    icon="Killer_Voice.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_HARDCORE",
    name="Hardcore",
    time="0:15", duration=5,
    icon="Hardcore.png",
    tags=[SpellTag.TANK_MIT],
    desc="Buster AoE on both tanks"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_VAMP_STOMP_1",
    name="Vamp Stomp",
    time="0:25", duration=5,
    icon="Vamp_Stomp.png",
    desc="Circle AoE spawning expanding ring"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_BLAST_BEAT_1",
    name="Blast Beat",
    time="0:34", duration=8,
    icon="Blast_Beat.png",
    desc="Mechanic Start"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_BRUTAL_RAIN_1",
    name="Brutal Rain",
    time="0:42", duration=4,
    icon="Brutal_Rain.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid Wide Damage"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_CROWD_KILL_1",
    name="Crowd Kill",
    time="2:27", duration=6,
    icon="Crowd_Kill.png",
    desc="Knockback from center"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_FINALE_FATALE_1",
    name="Finale Fatale",
    time="2:46", duration=5,
    icon="Finale_Fatale.png",
    tags=[SpellTag.RAID_MIT],
    desc="High Raid Damage"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_PULPING_PULSE",
    name="Pulping Pulse",
    time="2:57", duration=3,
    icon="Pulping_Pulse.png",
    desc="Stack/Spread mechanic"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_AETHERLETTING",
    name="Aetherletting Cones",
    time="2:58", duration=12,
    icon="Aetherletting_Cones.png",
    desc="Cones from boss + rotating adds"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_BRUTAL_RAIN_2",
    name="Brutal Rain",
    time="4:12", duration=5,
    icon="Brutal_Rain.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid Wide Damage"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_INSATIABLE_THIRST",
    name="Insatiable Thirst",
    time="4:25", duration=6,
    icon="Insatiable_Thirst.png",
    desc="Party soak mechanic"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_SADISTIC_SCREECH",
    name="Sadistic Screech",
    time="4:38", duration=6,
    icon="Sadistic_Screech.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid Damage + Dot"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_PLUMMET",
    name="Plummet x2 + Deadly Doornail",
    time="4:56", duration=5,
    icon="Plummet.png",
    desc="Tank towers and puddle AoEs. Towers spawn Fatal Flail when soaked"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_KILLER_VOICE_2",
    name="Killer Voice",
    time="5:00", duration=5,
    icon="Killer_Voice.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid damage"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_CROWD_KILL_2",
    name="Crowd Kill",
    time="6:05", duration=6,
    icon="Crowd_Kill.png",
    desc="Knockback from center"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_FINALE_FATALE_2",
    name="Finale Fatale",
    time="6:24", duration=5,
    icon="Finale_Fatale.png",
    tags=[SpellTag.RAID_MIT],
    desc="High Raid Damage"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_HELL_IN_A_CELL",
    name="Hell in a Cell",
    time="6:36", duration=5,
    icon="Hell_in_a_Cell.png",
    desc="4 tower soaks. Spawns Charnel Cell. Player soaking tower can't leave until add is killed"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_ULTRASONIC",
    name="Ultrasonic Spread/Amp",
    time="6:43", duration=6,
    icon="Ultrasonic_Spread.png",
    desc="Cone AoEs on 1 player of each role. Tank takes buster damage"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_BRUTAL_RAIN_3",
    name="Brutal Rain",
    time="8:14", duration=5,
    icon="Brutal_Rain.png",
    tags=[SpellTag.RAID_MIT],
    desc="Raid Wide Damage"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_VAMP_STOMP_2",
    name="Vamp Stomp",
    time="8:27", duration=5,
    icon="Vamp_Stomp.png",
    desc="Circle AoE spawning expanding ring"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_BLAST_BEAT_2",
    name="Blast Beat",
    time="8:34", duration=9,
    icon="Blast_Beat.png",
    desc="Mechanic Start"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_HALF_MOON",
    name="Half Moon",
    time="8:43", duration=5,
    icon="Half_Moon.png",
    desc="180 degree cleave"
)

VAMP_FATALE.add_cast(
    spell_id="M9S_HARDCORE_2",
    name="Hardcore",
    time="8:53", duration=5,
    icon="Hardcore.png",
    tags=[SpellTag.TANK_MIT],
    desc="Buster AoE on both tanks"
)
