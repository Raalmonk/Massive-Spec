"""Models for Top Rankings for a given Spec."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import datetime
import textwrap
import typing
from typing import Optional

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
    metric: str = "rdps"
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
    def get_query(self) -> str:
        """Return the Query to load the rankings for this Spec & Boss."""
        difficulty_id = DIFFICULTY_IDS.get(self.difficulty) or 101

        real_class_name = "Global"
        cn_class_name = "Global"
        spec_name = self.spec.name_slug_cap

        

        # 2. 定义查询构建函数 (支持传入不同的 class_name)
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

        # 3. 组合查询：Global 用具体名，CN 用 "Global"
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
        """Return a list of unique keys to identify existing reports."""
        for report in self.reports:
            for fight in report.fights:
                for player in fight.players:
                    key = (report.report_id, fight.fight_id, player.name)
                    yield key

    # 文件: lorgs/models/warcraftlogs_ranking.py

    def add_new_fight(self, ranking_data: wcl.CharacterRanking) -> None:
        report_data = ranking_data.report

        if not report_data:
            return

        # === 🔍 深度调试 START ===
        # 强制检查 combatantInfo 的状态
        info_list = ranking_data.combatantInfo
        info_len = len(info_list) if info_list else 0
        
        # 只打印前3个 fight 的详细信息，防止刷屏，但如果有问题一定要报出来
        if info_len == 0:
            print(f"[DEBUG-CRITICAL] Fight {report_data.fightID}: CombatantInfo is EMPTY! (Name: {ranking_data.name})")
        else:
            # 打印第一条数据看看长什么样，确认字段名是否正确
            first_item = info_list[0]
            print(f"[DEBUG-OK] Fight {report_data.fightID}: Found {info_len} combatants. Sample: {first_item}")
        # === 🔍 深度调试 END ===

        # skip hidden reports
        if ranking_data.hidden:
            return

        ################
        # Player
        # ... (后续代码保持不变)
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

        # Parse combatantInfo to add partners
        if ranking_data.combatantInfo:
            for combatant in ranking_data.combatantInfo:
                # Combatant is a dict
                name = combatant.get("name")
                if name == player.name:
                    continue

                spec_name = combatant.get("spec")
                class_name = combatant.get("type")

                # --- 🟢 新增 DEBUG ---
                # 打印出 WCL 返回的原始 Class 和 Spec 名字
                # 只打印一次或者前几次，避免日志爆炸
                if fight.fight_id % 10 == 0: # 稍微抽样一下
                     print(f"[DEBUG-Match] Try parsing: Name={name}, Class={class_name}, Spec={spec_name}")
                # ---------------------

                if spec_name and spec_name.lower() in ("dps", "healer", "tank"):
                     spec_name = class_name

                # 1. Try Strict Lookup (Class + Spec)
                spec = WowSpec.get(name_slug_cap=spec_name, wow_class__name_slug_cap=class_name)

                # 2. FIX: Fallback Lookup (Spec only) for FF14 compatibility
                if not spec:
                    spec = WowSpec.get(name_slug_cap=spec_name)

                if not spec:
                    # --- 🟢 新增 DEBUG ---
                    # 打印失败的情况
                    if fight.fight_id % 10 == 0:
                        print(f"[DEBUG-Match] FAILED to find spec for: {spec_name} (Class: {class_name})")
                    # ---------------------
                    continue

                # if spec.role.code != self.spec.role.code:
                #     continue

                p = Player(
                    source_id=combatant.get("id"),
                    name=name,
                    spec_slug=spec.full_name_slug,
                    total=0,
                )
                p.fight = fight
                fight.players.append(p)

        # Populate the composition list with spec slugs
        fight.composition = [p.spec_slug for p in fight.players]

        # === 🟢 新增 DEBUG 打印 (只针对 Spec Ranking) ===
        print(f"[DEBUG-SpecRanking] Fight ID: {fight.fight_id} | Composition Size: {len(fight.composition)}")
        print(f"[DEBUG-SpecRanking] Comp Details: {fight.composition}") # 如果想看详细内容就把这行解注
        # ===============================================
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

    def process_query_result(self, **query_result: typing.Any):
        """Process the Ranking Results."""
        # unwrap data
        encounter_data = query_result.get("worldData", {}).get("encounter", {})

        # === 🔍 DEBUG RAW JSON (新增) ===
        import json
        global_raw = encounter_data.get("global", {})
        rankings_raw = global_raw.get("rankings", [])
        
        print(f"[DEBUG-RAW] Rankings Count: {len(rankings_raw)}")
        if rankings_raw:
            first = rankings_raw[0]
            # 打印第一条数据的所有 Key，看看有没有 'combatantInfo'
            print(f"[DEBUG-RAW] First Item Keys: {list(first.keys())}")
            
            # 如果有 combatantInfo，打印它的类型和长度
            if "combatantInfo" in first:
                c_info = first["combatantInfo"]
                print(f"[DEBUG-RAW] 'combatantInfo' exists. Type: {type(c_info)}, Length: {len(c_info) if isinstance(c_info, list) else 'N/A'}")
            else:
                print(f"[DEBUG-RAW] ❌ 'combatantInfo' KEY IS MISSING in the API Response!")
        # ================================

        # 1. Global (Top 5)
        global_data = encounter_data.get("global", {})
        # ... 后续代码保持不变 ...
        global_rankings = wcl.CharacterRankings(**global_data).rankings[:20]

        # 2. CN (Top 10)
        cn_data = encounter_data.get("cn", {})
        cn_rankings = wcl.CharacterRankings(**cn_data).rankings[:10]

        # Log check to confirm we got CN names
        if cn_rankings:
            logger.info(f"[CN Data Check] First CN Player: {cn_rankings[0].name}")

        # Merge
        rankings = global_rankings + cn_rankings
        self.add_new_fights(rankings)
        self.post_init()

    async def load_rankings(self) -> None:
        """Fetch the current Ranking Data"""
        query = self.get_query()

        # Single query to Global API handles both regions now
        # We DO NOT need to switch endpoints or tokens.
        result = await self.client.query(query)
        self.process_query_result(**result)

    ############################################################################
    # Query: Fights
    #
    async def load_actors(self) -> None:
        """Load the Casts for all missing fights."""
        
        # [优化] 只加载主角的技能数据
        # 我们只关心当前排行榜对应的 Spec (比如 Astrologian)
        # 如果不加这个过滤，会加载所有 8 个队友的技能，导致 API 超限
        actors_to_load = [p for p in self.players if p.spec_slug == self.spec_slug]

        # 添加 Boss (只加载第一个 Boss 的完整时间轴，其他的只加载阶段)
        for i, fight in enumerate(self.fights):
            if not fight.boss:
                fight.boss = Boss(boss_slug=self.boss_slug)
                fight.boss.fight = fight

            if i == 0:
                fight.boss.query_mode = fight.boss.QueryModes.ALL
            else:
                fight.boss.query_mode = fight.boss.QueryModes.PHASES

            actors_to_load.append(fight.boss)

        # 过滤掉已经加载过的
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

        # 1. 加载排行榜 (此时可能丢失了队友信息)
        await self.load_rankings()
        self.reports = self.sort_reports(self.reports)

        # 2. 应用数量限制
        limit = limit or -1
        self.reports = self.reports[:limit]

        # 3. [核心修复] 检查并补全阵容
        # 如果战斗中玩家数量 <= 1，说明 combatantInfo 丢失，手动去抓 Summary
        fights_missing_comp = [f for f in self.fights if len(f.players) <= 1]
        
        if fights_missing_comp:
            logger.info(f"[Fallback] Fetching Composition for {len(fights_missing_comp)} fights (via Summary API)...")
            # 批量加载 Summary，这会填充 fight.players
            await self.load_many(fights_missing_comp, raise_errors=False)

        # 4. 加载技能数据
        await self.load_actors()
        
        logger.info("done")

        # 更新时间戳
        self.updated = datetime.datetime.now(datetime.timezone.utc)
        self.dirty = False

from lorgs.models.warcraftlogs_report import Report
SpecRanking.model_rebuild()