"""Legacy Ultimate encounter definitions for current FF Logs rankings."""

from lorgs.models.raid_zone import RaidZone

LEGACY_ULTIMATES_ZONE = RaidZone(
    id=59,
    name="Ultimates (Legacy)",
    icon="achievement_raid_ultimate.jpg",
)

THE_UNENDING_COIL_OF_BAHAMUT = LEGACY_ULTIMATES_ZONE.add_boss(
    id=1073,
    name="The Unending Coil of Bahamut",
    nick="UCOB",
    icon="boss_ucob.jpg",
)

THE_WEAPONS_REFRAIN = LEGACY_ULTIMATES_ZONE.add_boss(
    id=1074,
    name="The Weapon's Refrain",
    nick="UWU",
    icon="boss_uwu.jpg",
)

THE_EPIC_OF_ALEXANDER = LEGACY_ULTIMATES_ZONE.add_boss(
    id=1075,
    name="The Epic of Alexander",
    nick="TEA",
    icon="boss_tea.jpg",
)

DRAGONSONGS_REPRISE = LEGACY_ULTIMATES_ZONE.add_boss(
    id=1076,
    name="Dragonsong's Reprise",
    nick="DSR",
    icon="boss_dsr.jpg",
)

THE_OMEGA_PROTOCOL = LEGACY_ULTIMATES_ZONE.add_boss(
    id=1077,
    name="The Omega Protocol",
    nick="TOP",
    icon="boss_top.jpg",
)
