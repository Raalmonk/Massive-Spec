"""Dancing Mad Timeline."""

from lorgs.models.raid_zone import RaidZone

DANCING_MAD_ZONE = RaidZone(
    id=76,
    name="Dancing Mad",
    icon="boss_dancing_mad.jpg",
)

# FFLogs uses the provided zone/ranking page id for this Ultimate ranking path.
DANCING_MAD = DANCING_MAD_ZONE.add_boss(
    id=76,
    name="Dancing Mad",
    nick="DM",
    icon="boss_dancing_mad.jpg",
)

# TODO: Fill exact FFLogs phase trigger ability IDs when confirmed.
# DANCING_MAD.add_phase(name="P2", spell_id=0, event_type="cast")
# DANCING_MAD.add_phase(name="P3", spell_id=0, event_type="cast")
