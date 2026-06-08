"""Dancing Mad Timeline."""

from lorgs.boss_timeline import BossTimelineEvent
from lorgs.models.raid_zone import RaidZone

DANCING_MAD_ZONE = RaidZone(
    id=76,
    name="Dancing Mad",
    icon="boss_dancing_mad.jpg",
)

# FFLogs uses zone/page id 76 for this Ultimate ranking path.
# GraphQL encounter ranking queries use the encounter id from the ranking URL.
DANCING_MAD = DANCING_MAD_ZONE.add_boss(
    id=1085,
    name="Dancing Mad",
    nick="DM",
    icon="boss_dancing_mad.jpg",
)

# FF Logs should provide Dancing Mad phase intervals natively via report phases/phaseTransitions
# once public kill logs exist. Do not add manual trigger spell IDs here.

DANCING_MAD_BOSS_TIMELINE = [
    BossTimelineEvent(id="dm-kefka-graven-image-1", name="Graven Image", time=29.200, duration=2.70, type="mech"),
    BossTimelineEvent(id="dm-kefka-graven-image-2", name="Graven Image", time=80.284, duration=2.70, type="mech"),
    BossTimelineEvent(id="dm-kefka-graven-image-3", name="Graven Image", time=163.828, duration=2.70, type="mech"),
    BossTimelineEvent(id="dm-kefka-forsaken-1", name="Forsaken", time=235.596, duration=6.70, type="mech"),
    BossTimelineEvent(id="dm-kefka-light-of-judgment", name="Light of Judgment", time=341.888, duration=4.70, type="mech"),
    BossTimelineEvent(id="dm-kefka-decisive-battle-1", name="the Decisive Battle", time=430.947, duration=2.70, type="mech"),
    BossTimelineEvent(id="dm-kefka-decisive-battle-2", name="the Decisive Battle", time=545.267, duration=2.70, type="mech"),
    BossTimelineEvent(id="dm-kefka-celestriad", name="Celestriad", time=958.582, duration=4.70, type="mech"),
    BossTimelineEvent(id="dm-kefka-forsaken-2", name="Forsaken", time=1058.663, duration=9.70, type="mech"),
    BossTimelineEvent(id="dm-tb-revolting-ruin-iii-1", name="Revolting Ruin III", time=15.235, duration=4.70, type="tb"),
    BossTimelineEvent(id="dm-tb-hyperdrive-1", name="Hyperdrive", time=65.900, duration=1, type="tb"),
    BossTimelineEvent(id="dm-tb-revolting-ruin-iii-2", name="Revolting Ruin III", time=97.428, duration=4.70, type="tb"),
    BossTimelineEvent(id="dm-tb-hyperdrive-2", name="Hyperdrive", time=135.670, duration=1, type="tb"),
    BossTimelineEvent(id="dm-tb-ultimate-embrace-1", name="Ultimate Embrace", time=220.366, duration=4.70, type="tb"),
    BossTimelineEvent(id="dm-tb-wings-of-destruction", name="Wings of Destruction", time=370.372, duration=3.70, type="tb"),
    BossTimelineEvent(id="dm-tb-ultimate-embrace-2", name="Ultimate Embrace", time=377.671, duration=4.70, type="tb"),
    BossTimelineEvent(id="dm-tb-thunder-iii-1a", name="Thunder III", time=478.683, duration=4.70, type="tb"),
    BossTimelineEvent(id="dm-tb-thunder-iii-2a", name="Thunder III", time=537.307, duration=4.70, type="tb"),
    BossTimelineEvent(id="dm-tb-thunder-iii-3a", name="Thunder III", time=554.465, duration=4.70, type="tb"),
    BossTimelineEvent(id="dm-tb-thunder-iii-4a", name="Thunder III", time=596.033, duration=4.70, type="tb"),
    BossTimelineEvent(id="dm-tb-thunder-iii-5a", name="Thunder III", time=637.277, duration=4.70, type="tb"),
    BossTimelineEvent(id="dm-tb-fell-forces-1", name="Fell Forces x3", time=912.132, duration=1, type="tb"),
    BossTimelineEvent(id="dm-tb-flare-1", name="Flare", time=937.767, duration=1, type="tb"),
    BossTimelineEvent(id="dm-tb-chaotic-flare-1", name="Chaotic Flare", time=940.941, duration=1, type="tb"),
    BossTimelineEvent(id="dm-tb-flare-diffusion-1", name="Flare Diffusion", time=944.426, duration=1, type="tb"),
    BossTimelineEvent(id="dm-tb-chaotic-holy-1", name="Chaotic Holy", time=944.426, duration=1, type="tb"),
    BossTimelineEvent(id="dm-tb-fell-forces-2", name="Fell Forces x2", time=949.075, duration=1, type="tb"),
    BossTimelineEvent(id="dm-tb-fell-forces-3", name="Fell Forces x2", time=994.031, duration=1, type="tb"),
    BossTimelineEvent(id="dm-tb-flare-2", name="Flare", time=1029.820, duration=1, type="tb"),
    BossTimelineEvent(id="dm-tb-chaotic-flare-2", name="Chaotic Flare", time=1032.989, duration=1, type="tb"),
    BossTimelineEvent(id="dm-tb-flare-diffusion-2", name="Flare Diffusion", time=1036.466, duration=1, type="tb"),
    BossTimelineEvent(id="dm-tb-chaotic-holy-2", name="Chaotic Holy", time=1036.466, duration=1, type="tb"),
    BossTimelineEvent(id="dm-tb-fell-forces-4", name="Fell Forces x3", time=1041.101, duration=1, type="tb"),
]

object.__setattr__(DANCING_MAD, "boss_timeline", DANCING_MAD_BOSS_TIMELINE)
