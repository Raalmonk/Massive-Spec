"""Defines which Raid/Dungeon the current Season includes."""

# from lorgs.data.expansions.the_war_within.seasons.tww_s1 import TWW_SEASON1
# from lorgs.data.expansions.the_war_within.seasons.tww_s2 import TWW_SEASON2
# from lorgs.data.expansions.the_war_within.seasons.tww_s3 import TWW_SEASON3

from lorgs.models.season import Season
from lorgs.data.expansions.dawntrail import ARCADION_HEAVYWEIGHT

DAWNTRAIL_S1 = Season(
    slug="dawntrail-s1",
    name="Dawntrail Season 1",
    ilvl=730,
    raids=[ARCADION_HEAVYWEIGHT],
)

ALL_SEASONS = [
    DAWNTRAIL_S1,
    # TWW_SEASON1,
    # TWW_SEASON2,
    # TWW_SEASON3,
]


CURRENT_SEASON = DAWNTRAIL_S1
CURRENT_SEASON.activate()


__all__ = [
    "ALL_SEASONS",
    "CURRENT_SEASON",
]
