"""Dancing Mad Timeline."""

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
