"""Models for Top Rankings for a given Spec."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import textwrap
import typing
from typing import Dict, Tuple

# IMPORT THIRD PARTY LIBRARIES
import pydantic

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
    
    # 绝对真理缓存 (不序列化)
    _official_dps_cache: Dict[Tuple[int, str], float] = pydantic.PrivateAttr(default_factory=dict)

    key: typing.ClassVar[str] = "{spec_slug}/{boss_slug}__{difficulty}__{metric}"

    def post_init(self) -> None:
        for report in self.reports:
            report.post_init()

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

    # ==========================================================================
    # [FIX] 排序逻辑重构
    # 1. 改为实例方法，以便访问 self._official_dps_cache
    # 2. 只依据“主角”的“官方DPS”进行排序，彻底屏蔽队友数据干扰
    # ==========================================================================
    def sort_reports(self, reports: list[Report]) -> list[Report]:
        """Sort the reports in place by the highest dps player."""
        
        def normalize_name(n):
            return n.split("-")[0].strip() if "-" in n else n.strip()

        def get_score(report: Report) -> float:
            if not report.fights:
                return 0.0
            
            # 这里的 fight[0] 是 Report 的主体战斗
            fight = report.fights[0]
            if not fight.players:
                return 0.0
            
            # [关键] players[0] 永远是该 Ranking 条目的主角
            # 我们只关心主角的排名，队友打得再高也不应该影响这份报告的排序
            main_player = fight.players[0]
            
            # 尝试从官方缓存获取绝对正确的数值
            simple_key = (fight.fight_id, normalize_name(main_player.name))
            raw_key = (fight.fight_id, main_player.name)
            
            cached_score = self._official_dps_cache.get(simple_key) or self._official_dps_cache.get(raw_key)
            
            if cached_score:
                return cached_score
            
            # 如果缓存里没有(理论上不可能)，退化为使用本地值
            return main_player.total

        return sorted(reports, key=get_score, reverse=True)

    def get_query(self) -> str:
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
        if not report_data: return
        if ranking_data.hidden: return

        # [关键] 主角总是第一个被添加
        player = Player(
            name=ranking_data.name,
            total=ranking_data.amount,
            spec_slug=self.spec_slug,
        )

        fight = Fight(
            fight_id=report_data.fightID,
            start_time=ranking_data.startTime,
            duration=ranking_data.duration,
            players=[player],
        )

        if ranking_data.combatantInfo:
            for combatant in ranking_data.combatantInfo:
                name = combatant.get("name")
                if name == player.name: continue

                spec_name = combatant.get("spec")
                class_name = combatant.get("type")
                if spec_name and spec_name.lower() in ("dps", "healer", "tank"):
                     spec_name = class_name

                spec = WowSpec.get(name_slug_cap=spec_name, wow_class__name_slug_cap=class_name)
                if not spec: spec = WowSpec.get(name_slug_cap=spec_name)
                if not spec: continue

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
            if key in old_reports: continue
            self.add_new_fight(ranking_data)

    def process_query_result(self, **query_result: typing.Any):
        encounter_data = query_result.get("worldData", {}).get("encounter", {})
        
        global_data = encounter_data.get("global", {})
        global_rankings = wcl.CharacterRankings(**global_data).rankings 

        cn_data = encounter_data.get("cn", {})
        cn_rankings = wcl.CharacterRankings(**cn_data).rankings

        rankings = global_rankings + cn_rankings
        
        # 填充缓存
        self._official_dps_cache = {}
        def normalize_name(n):
            return n.split("-")[0].strip() if "-" in n else n.strip()

        for r in rankings:
            simple_key = (r.report.fightID, normalize_name(r.name))
            raw_key = (r.report.fightID, r.name)
            self._official_dps_cache[simple_key] = r.amount
            self._official_dps_cache[raw_key] = r.amount

        self.add_new_fights(rankings)
        self.post_init()

    async def load_rankings(self) -> None:
        query = self.get_query()
        result = await self.client.query(query)
        self.process_query_result(**result)

    async def load_actors(self) -> None:
        actors_to_load = [p for p in self.players if p.spec_slug == self.spec_slug]
        for i, fight in enumerate(self.fights):
            if not fight.boss:
                fight.boss = Boss(boss_slug=self.boss_slug)
                fight.boss.fight = fight
            if i == 0: fight.boss.query_mode = fight.boss.QueryModes.ALL
            else: fight.boss.query_mode = fight.boss.QueryModes.PHASES
            actors_to_load.append(fight.boss)

        actors_to_load = [actor for actor in actors_to_load if actor and not actor.casts]
        logger.info(f"load {len(actors_to_load)} players/bosses")
        if not actors_to_load: return
        await self.load_many(actors_to_load, raise_errors=False)

    async def load(self, limit=50, clear_old=False) -> None:
        logger.info(f"{self.boss.name} vs. {self.spec.name} {self.spec.wow_class.name} START | limit={limit} | clear_old={clear_old}")

        if clear_old:
            self.reports = []
            self._official_dps_cache = {}

        await self.load_rankings()
        
        # 初次排序 (此时本地 total 是准确的)
        self.reports = self.sort_reports(self.reports)

        limit = limit or -1
        self.reports = self.reports[:limit]

        fights_missing_comp = [f for f in self.fights if len(f.players) <= 1]
        if fights_missing_comp:
            logger.info(f"[Fallback] Fetching Composition for {len(fights_missing_comp)} fights...")
            await self.load_many(fights_missing_comp, raise_errors=False)

        # 这一步会弄乱 total，但是无所谓，我们后面会修，而且排序已经不再依赖它
        await self.load_actors()
        
        # [Final Fix]
        def normalize_name(n):
            return n.split("-")[0].strip() if "-" in n else n.strip()

        restore_count_final = 0
        for report in self.reports:
            for fight in report.fights:
                for player in fight.players:
                    key_simple = (fight.fight_id, normalize_name(player.name))
                    key_raw = (fight.fight_id, player.name)
                    
                    official_val = self._official_dps_cache.get(key_simple) or self._official_dps_cache.get(key_raw)
                    
                    if official_val is not None:
                        if abs(player.total - official_val) > 0.1: 
                            player.total = official_val
                            restore_count_final += 1
        
        if restore_count_final > 0:
            logger.info(f"[DPS Final Fix] Corrected DPS for {restore_count_final} players.")
        
        # [重要] 最后再次排序！
        # 确保哪怕有队友数据异常，报告的顺序依然严格遵循“主角”的官方 DPS
        self.reports = self.sort_reports(self.reports)
        
        logger.info("done")
        self.updated = datetime.datetime.now(datetime.timezone.utc)
        self.dirty = False

from lorgs.models.warcraftlogs_report import Report
SpecRanking.model_rebuild()