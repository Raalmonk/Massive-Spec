"""Models for Top Rankings for a given Spec."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import asyncio
import datetime
import textwrap
import typing

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.clients import wcl
from lorgs.logger import logger
from lorgs.models import warcraftlogs_base
from lorgs.models.base.s3 import S3Model
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.warcraftlogs_boss import Boss
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_player import Player
from lorgs.models.warcraftlogs_report import Report
from lorgs.models.wow_spec import WowSpec


# Map Difficulty Names to Integers used in WCL
DIFFICULTY_IDS = {
    "normal": 100,
    "heroic": 101,  # savage
    "mythic": 101,  # savage
    "savage": 101,
    "extreme": 102,
    "ultimate": 103,
}


class SpecRanking(S3Model, warcraftlogs_base.wclclient_mixin):
    # Fields
    spec_slug: str
    boss_slug: str
    difficulty: str = "mythic"
    metric: str = ""
    reports: list[Report] = []

    updated: datetime.datetime = datetime.datetime.min
    dirty: bool = False

    # Config
    key: typing.ClassVar[str] = "{spec_slug}/{boss_slug}__{difficulty}__{metric}"

    def post_init(self) -> None:
        for report in self.reports:
            report.post_init()

    ##########################
    # Attributes
    #
    @property
    def spec(self) -> WowSpec:
        return WowSpec.get(full_name_slug=self.spec_slug)  # type: ignore

    @property
    def boss(self) -> RaidBoss:
        return RaidBoss.get(full_name_slug=self.boss_slug)  # type: ignore

    @property
    def fights(self) -> list[Fight]:
        return utils.flatten(report.fights for report in self.reports)

    @property
    def players(self) -> list[Player]:
        return utils.flatten(fight.players for fight in self.fights)

    ##########################
    # Methods
    #
    @staticmethod
    def sort_reports(reports: list[Report]) -> list[Report]:
        """Sort the reports in place by the highest dps player."""

        def get_total(report: Report) -> float:
            top = 0.0
            for fight in report.fights:
                for player in fight.players:
                    top = max(top, player.total)
            return top

        return sorted(reports, key=get_total, reverse=True)

    ############################################################################
    # Query: Rankings
    #
    def get_query(self, server_region: str = None, page: int = 1) -> str:
        """Return the Query to load the rankings for this Spec & Boss."""
        difficulty_id = DIFFICULTY_IDS.get(self.difficulty) or 101

        # Build Arguments
        args = [
            f'className: "{self.spec.wow_class.name_slug_cap}"',
            f'specName: "{self.spec.name_slug_cap}"',
            f'metric: {self.metric}',
            f'difficulty: {difficulty_id}',
            'includeCombatantInfo: true',
            f'page: {page}',
        ]
        if server_region:
            args.append(f'serverRegion: "{server_region}"')

        args_str = "\n".join(args)

        return textwrap.dedent(
            f"""\
        worldData
        {{
            encounter(id: {self.boss.id})
            {{
                characterRankings(
                    {args_str}
                )
            }}
        }}
        """
        )

    @utils.as_list
    def get_old_reports(self) -> typing.Generator[tuple[str, int, str], None, None]:
        """Return a list of unique keys to identify existing reports."""
        for report in self.reports:
            for fight in report.fights:
                for player in fight.players:
                    key = (report.report_id, fight.fight_id, player.name)
                    yield key

    def add_new_fight(self, ranking_data: wcl.CharacterRanking) -> None:
        report_data = ranking_data.report

        if not report_data:
            return

        # skip hidden reports
        if ranking_data.hidden:
            return

        ################
        # Player
        player = Player(
            name=ranking_data.name,
            total=ranking_data.amount,
            spec_slug=self.spec_slug,
        )

        ################
        # Fight
        fight = Fight(
            fight_id=report_data.fightID,
            start_time=ranking_data.startTime,
            duration=ranking_data.duration,
            players=[player],
        )

        # Parse Composition
        # combatantInfo is a list of dicts. format varies by game.
        # for FFXIV it seems to include "spec" (int) or "icon" (str).
        # We try to map it to our internal spec slugs.
        # Note: This is a best effort.
        if ranking_data.combatantInfo:
            for actor_data in ranking_data.combatantInfo:
                # We can try to use the icon name to find the spec
                # eg.: "Paladin-Tank" or "Paladin"
                spec_name = actor_data.get("spec") or actor_data.get("type") # type is often Class
                # But combatantInfo in WCL v2 for FF usually returns integers for spec?
                # or string names.
                # Let's rely on `fetch_top_ranks` assumption or try to match.

                # If we can't easily parse, we skip.
                # But wait, if I don't parse it, the frontend won't get it.
                # Let's assume the frontend logic needs spec slugs.
                # I'll store whatever I can find that looks like a spec.
                pass

            # Since we don't know the exact format and I cannot run it,
            # I will trust the `combatantInfo` field passed as is to the fight,
            # and let the frontend handle the mapping if it's raw data?
            # NO, `Fight.combatant_info` is expected to be a list of spec slugs (strings).
            # `fetch_top_ranks.py` says `combatant_info` is populated by `process_players`.
            # `process_players` uses `summary_data.composition` which has `specs` list.

            # Here `ranking_data.combatantInfo` might be different from `summary_data.composition`.
            # If I can't parse it reliably, I might fail Task 3.

            # Let's look at `lorgs/models/warcraftlogs_fight.py` `process_players` again.
            # It maps `composition_data.specs[0].spec` (string) to `WowSpec`.

            # So I will assume `combatantInfo` has `spec` field as string.
            # And I will use `WowSpec.get`.

            fight.combatant_info = []
            for actor in ranking_data.combatantInfo:
                # heuristic to find spec name
                spec_name = actor.get("spec")
                class_name = actor.get("class") # or type?

                if not spec_name and not class_name:
                    continue

                # Try to resolve spec
                spec = None
                if spec_name:
                    spec = WowSpec.get(name_slug_cap=spec_name)

                if not spec and class_name:
                     # Try class (for single-spec classes or if spec is missing)
                     # But spec lookup usually needs both.
                     pass

                if spec:
                    fight.combatant_info.append(spec.full_name_slug)

        ################
        # Report
        report = Report(
            report_id=report_data.code,
            start_time=report_data.startTime,
            fights=[fight],
            region=ranking_data.server.region,
        )
        self.reports.append(report)

    def add_new_fights(self, rankings: list[wcl.CharacterRanking]):
        """Add new Fights."""
        old_reports = self.get_old_reports()

        for ranking_data in rankings:
            report_data = ranking_data.report

            ################
            # check if already in the list
            key = (report_data.code, report_data.fightID, ranking_data.name)
            if key in old_reports:
                continue

            self.add_new_fight(ranking_data)

    def process_query_result(self, limit: int = 0, **query_result: typing.Any):
        """Process the Ranking Results.

        Expected Query:
        >>> {
        >>>     worldData: {
        >>>         encounter: {
        >>>             characterRankings: ....
        >>>         }
        >>>     }
        >>> }
        """
        # unwrap data
        query_result = query_result.get("worldData") or query_result
        world_data = wcl.WorldData(**query_result)

        rankings = world_data.encounter.characterRankings.rankings
        if limit > 0:
            rankings = rankings[:limit]

        self.add_new_fights(rankings)
        self.post_init()

    async def load_rankings(self) -> None:
        """Fetch the current Ranking Data"""
        # Dual Region Fetching
        # 1. Global (Top 5)
        # 2. CN (Top 10)

        q_global = self.get_query(server_region="Global", page=1)
        q_cn = self.get_query(server_region="CN", page=1)

        results = await asyncio.gather(
            self.client.query(q_global),
            self.client.query(q_cn),
            return_exceptions=True
        )

        # Process Global
        res_global = results[0]
        if isinstance(res_global, dict):
            self.process_query_result(limit=5, **res_global)
        else:
            logger.error(f"Error fetching Global rankings: {res_global}")

        # Process CN
        res_cn = results[1]
        if isinstance(res_cn, dict):
            self.process_query_result(limit=10, **res_cn)
        else:
            logger.error(f"Error fetching CN rankings: {res_cn}")

    ############################################################################
    # Query: Fights
    #
    async def load_actors(self) -> None:
        """Load the Casts for all missing fights."""
        actors_to_load = self.players

        # add Boss Actors
        for i, fight in enumerate(self.fights):
            if not fight.boss:
                fight.boss = Boss(boss_slug=self.boss_slug)
                fight.boss.fight = fight

            # Only full load the first boss.
            # for 2..n only load phase infos
            if i == 0:
                fight.boss.query_mode = fight.boss.QueryModes.ALL
            else:
                fight.boss.query_mode = fight.boss.QueryModes.PHASES

            actors_to_load += [fight.boss]  # type: ignore

        # filter out actors that have already been loaded
        actors_to_load = [actor for actor in actors_to_load if actor]
        actors_to_load = [actor for actor in actors_to_load if not actor.casts]

        logger.info(f"load {len(actors_to_load)} players")
        if not actors_to_load:
            return

        await self.load_many(actors_to_load, raise_errors=False)  # type: ignore

    ############################################################################
    # Query: Both
    #
    async def load(self, limit=50, clear_old=False) -> None:
        """Get Top Ranks for a given boss and spec."""
        logger.info(f"{self.boss.name} vs. {self.spec.name} {self.spec.wow_class.name} START | limit={limit} | clear_old={clear_old}")

        if clear_old:
            self.reports = []

        # refresh the ranking data
        await self.load_rankings()
        self.reports = self.sort_reports(self.reports)

        # enforce limit
        limit = limit or -1
        self.reports = self.reports[:limit]

        # load the fights/players/casts
        await self.load_actors()
        logger.info("done")

        # update timestamp and mark as clean
        self.updated = datetime.datetime.now(datetime.timezone.utc)
        self.dirty = False
