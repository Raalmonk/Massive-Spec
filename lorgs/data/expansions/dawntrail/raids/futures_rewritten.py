"""Future Rewritten Timeline."""

from lorgs.models.raid_zone import RaidZone

FUTURES_REWRITTEN_ZONE = RaidZone(
    id=65,
    name="Future Rewritten",
    icon="boss_futures_rewritten.jpg",
)

# FFLogs uses the provided zone/ranking page id for this Ultimate ranking path.
# The boss name is pluralized to preserve the requested slug; nick is the display label.
# GraphQL encounter ranking queries use the encounter id, while the zone/page id remains 65.
FUTURES_REWRITTEN = FUTURES_REWRITTEN_ZONE.add_boss(
    id=1079,
    name="Futures Rewritten",
    nick="Future Rewritten",
    icon="boss_futures_rewritten.jpg",
)

# FF Logs provides FRU phase intervals natively via report phases/phaseTransitions.
# Do not add manual trigger spell IDs here; they drift from the official phase dropdown.
