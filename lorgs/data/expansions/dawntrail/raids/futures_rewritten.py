"""Future Rewritten Timeline."""

from lorgs.models.raid_zone import RaidZone

FUTURES_REWRITTEN_ZONE = RaidZone(
    id=65,
    name="Future Rewritten",
    icon="boss_futures_rewritten.jpg",
)

# FFLogs uses the provided zone/ranking page id for this Ultimate ranking path.
# The boss name is pluralized to preserve the requested slug; nick is the display label.
FUTURES_REWRITTEN = FUTURES_REWRITTEN_ZONE.add_boss(
    id=65,
    name="Futures Rewritten",
    nick="Future Rewritten",
    icon="boss_futures_rewritten.jpg",
)

# TODO: Fill exact FFLogs phase trigger ability IDs when confirmed.
# FUTURES_REWRITTEN.add_phase(name="P2", spell_id=0, event_type="cast")
# FUTURES_REWRITTEN.add_phase(name="P3", spell_id=0, event_type="cast")
