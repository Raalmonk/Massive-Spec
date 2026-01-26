"""Models for Top Rankings for a given Spec."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import textwrap
import typing
from typing import Optional, Dict, Tuple

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
    "heroic": 101,
    "mythic": 101,
    "savage": 101,
    "extreme": 102,
    "ultimate": 103,
}


class SpecRanking(S3Model, warcraftlogs_base.wclclient_mixin):
    # Fields
    spec_slug: str
    boss_slug: str
    difficulty: str = "mythic"
    metric: str = "rdps"
    reports: list[Report] = []

    updated: datetime.datetime = datetime.datetime.min
    dirty: bool = False
    
    # [新增] 专门用来存从 API 拿到的绝对正确的 DPS
    # Key: (fight_id, player_name_simple) -> Value: correct_dps
    official_dps_cache: Dict[Tuple[int, str], float] = {}

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

    def get_query(self) -> str:
        """Return the Query to load the rankings for this Spec & Boss."""
        difficulty_id = DIFFICULTY_IDS.get(self.difficulty) or 101
        real_class_name = "Global"
        cn_class_name = "Global"
        spec_name = self.spec.name_slug_cap

        def build_rankings_query(class_name_arg: str, extra_args: str = ""):
            return f"""
                characterRankings(
                    className: "{class_name_arg}"
                    specName: "{spec_name}"
                    metric: {self.metric}
                    difficulty: {difficulty_id}
                    includeCombatantInfo: true
                    {extra_args}
                )
            """

        return textwrap.dedent(
            f"""\
        worldData
        {{
            encounter(id: {self.boss.id})
            {{
                global: {build_rankings_query(real_class_name)}
                cn: {build_rankings_query(cn_class_name, 'partition: 3, serverRegion: "CN"')}
            }}
        }}
        """
        )

    @utils.as_list
    def get_old_reports(self) -> typing.Generator[tuple[str, int, str], None, None]:
        for report in self.reports:
            for fight in report.fights:
                for player in fight.players:
                    key = (report.report_id, fight.fight_id, player.name)
                    yield key

    def add_new_fight(self, ranking_data: wcl.CharacterRanking) -> None:
        report_data = ranking_data.report
        if not report_data:
            return
        if ranking_data.hidden:
            return

        # Player
        player = Player(
            name=ranking_data.name,
            total=ranking_data.amount,
            spec_slug=self.spec_slug,
        )

        # Fight
        fight = Fight(
            fight_id=report_data.fightID,
            start_time=ranking_data.startTime,
            duration=ranking_data.duration,
            players=[player],
        )

        # Parse combatantInfo to add partners
        if ranking_data.combatantInfo:
            for combatant in ranking_data.combatantInfo:
                name = combatant.get("name")
                if name == player.name:
                    continue

                spec_name = combatant.get("spec")
                class_name = combatant.get("type")

                if spec_name and spec_name.lower() in ("dps", "healer", "tank"):
                     spec_name = class_name

                spec = WowSpec.get(name_slug_cap=spec_name, wow_class__name_slug_cap=class_name)
                if not spec:
                    spec = WowSpec.get(name_slug_cap=spec_name)
                if not spec:
                    continue

                p = Player(
                    source_id=combatant.get("id"),
                    name=name,
                    spec_slug=spec.full_name_slug,
                    total=0,
                )
                p.fight = fight
                fight.players.append(p)

        fight.composition = [p.spec_slug for p in fight.players]
        
        report = Report(
            report_id=report_data.code,
            start_time=report_data.startTime,
            fights=[fight],
            region=ranking_data.server.region,
        )
        self.reports.append(report)

    def add_new_fights(self, rankings: list[wcl.CharacterRanking]):
        old_reports = self.get_old_reports()
        for ranking_data in rankings:
            report_data = ranking_data.report
            key = (report_data.code, report_data.fightID, ranking_data.name)
            if key in old_reports:
                continue
            self.add_new_fight(ranking_data)

    ############################################################################
    # Query: Rankings
    #
    def process_query_result(self, **query_result: typing.Any):
        """Process the Ranking Results."""
        encounter_data = query_result.get("worldData", {}).get("encounter", {})

        global_data = encounter_data.get("global", {})
        global_rankings = wcl.CharacterRankings(**global_data).rankings 

        cn_data = encounter_data.get("cn", {})
        cn_rankings = wcl.CharacterRankings(**cn_data).rankings

        # Merge
        rankings = global_rankings + cn_rankings
        
        # [核心] 构建绝对真理缓存
        # 无论后续把 total 改成什么样，这个字典里的值永远是 WCL 官方榜单上的值
        self.official_dps_cache = {}
        
        def normalize_name(n):
            # 去除服务器名，只留 ID
            return n.split("-")[0].strip() if "-" in n else n.strip()

        for r in rankings:
            # Key: (FightID, NormalizedName)
            # 这样不管是 "引力同频" 还是 "引力同频-Server"，都能对上
            key = (r.report.fightID, normalize_name(r.name))
            self.official_dps_cache[key] = r.amount
            
            # 为了保险，把不去掉服务器名的也存一份
            key_raw = (r.report.fightID, r.name)
            self.official_dps_cache[key_raw] = r.amount

        self.add_new_fights(rankings)
        self.post_init()

    async def load_rankings(self) -> None:
        """Fetch the current Ranking Data"""
        query = self.get_query()
        result = await self.client.query(query)
        self.process_query_result(**result)

    ############################################################################
    # Query: Fights
    #
    async def load_actors(self) -> None:
        """Load the Casts for all missing fights."""
        actors_to_load = [p for p in self.players if p.spec_slug == self.spec_slug]
        for i, fight in enumerate(self.fights):
            if not fight.boss:
                fight.boss = Boss(boss_slug=self.boss_slug)
                fight.boss.fight = fight
            if i == 0:
                fight.boss.query_mode = fight.boss.QueryModes.ALL
            else:
                fight.boss.query_mode = fight.boss.QueryModes.PHASES
            actors_to_load.append(fight.boss)

        actors_to_load = [actor for actor in actors_to_load if actor and not actor.casts]
        logger.info(f"load {len(actors_to_load)} players/bosses")
        if not actors_to_load:
            return
        await self.load_many(actors_to_load, raise_errors=False)

    ############################################################################
    # Query: Both
    #
    async def load(self, limit=50, clear_old=False) -> None:
        """Get Top Ranks for a given boss and spec."""
        logger.info(f"{self.boss.name} vs. {self.spec.name} {self.spec.wow_class.name} START | limit={limit} | clear_old={clear_old}")

        if clear_old:
            self.reports = []
            self.official_dps_cache = {} # 清空缓存

        # 1. 加载排行榜 (此时 official_dps_cache 被填充)
        await self.load_rankings()
        self.reports = self.sort_reports(self.reports)

        # 2. 应用数量限制
        limit = limit or -1
        self.reports = self.reports[:limit]

        # 3. 补全阵容
        fights_missing_comp = [f for f in self.fights if len(f.players) <= 1]
        if fights_missing_comp:
            logger.info(f"[Fallback] Fetching Composition for {len(fights_missing_comp)} fights...")
            await self.load_many(fights_missing_comp, raise_errors=False)

        # 4. 加载技能数据 (会把 dps 算错)
        await self.load_actors()
        
        # ============================================================
        # [Final Fix v6] 使用 API 原始数据覆盖
        # ============================================================
        def normalize_name(n):
            return n.split("-")[0].strip() if "-" in n else n.strip()

        restore_count_final = 0
        for report in self.reports:
            for fight in report.fights:
                for player in fight.players:
                    # 尝试匹配
                    key_simple = (fight.fight_id, normalize_name(player.name))
                    key_raw = (fight.fight_id, player.name)
                    
                    official_val = self.official_dps_cache.get(key_simple) or self.official_dps_cache.get(key_raw)
                    
                    if official_val is not None:
                        if abs(player.total - official_val) > 1.0: 
                            if "引力" in player.name or "偷心" in player.name:
                                logger.info(f"[DPS Fix] RESTORING {player.name}: {player.total} -> {official_val}")
                            
                            player.total = official_val
                            restore_count_final += 1
        
        if restore_count_final > 0:
            logger.info(f"[DPS Final Fix] Corrected DPS for {restore_count_final} players to match Leaderboard.")
        # ============================================================
        
        logger.info("done")
        self.updated = datetime.datetime.now(datetime.timezone.utc)
        self.dirty = False

from lorgs.models.warcraftlogs_report import Report
SpecRanking.model_rebuild()