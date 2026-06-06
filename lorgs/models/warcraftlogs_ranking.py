"""Models for Top Rankings for a given Spec."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import asyncio
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
    "ultimate": 100,
}

RANKING_REGION_LIMITS = {
    "global": 65,
    "cn": 25,
    "kr": 10,
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
    def _normalize_name(name: str) -> str:
        """Helper: Normalize player name by removing server suffix."""
        if not name:
            return ""
        # Split by '-' and take the first part (Name), strip whitespace
        return name.split("-")[0].strip()

    @staticmethod
    def sort_reports(reports: list[Report]) -> list[Report]:
        """Sort the reports in place by the highest dps player."""

        def get_total(report: Report) -> float:
            top = 0.0
            for fight in report.fights:
                # 此时 players[0] 已经被修正为正确的主角 (高DPS)，其他的都是0
                if fight.players:
                    top = max(top, fight.players[0].total)
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
                global: {build_rankings_query(real_class_name, 'partition: 7')}
                cn: {build_rankings_query(cn_class_name, 'partition: 3, serverRegion: "CN"')}
                kr: {build_rankings_query(real_class_name, 'partition: 5')}
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
        # Player (Primary Ranker - ALWAYS Index 0 initially)
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

        # Populate the composition list with spec slugs
        fight.composition = [p.spec_slug for p in fight.players]

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
            key = (report_data.code, report_data.fightID, ranking_data.name)
            if key in old_reports:
                continue
            self.add_new_fight(ranking_data)

    def process_query_result(self, **query_result: typing.Any):
        """Process the Ranking Results."""
        encounter_data = query_result.get("worldData", {}).get("encounter", {})

        def valid_rankings(rankings: list[wcl.CharacterRanking]) -> list[wcl.CharacterRanking]:
            return [ranking for ranking in rankings if not ranking.hidden and ranking.report]

        global_data = encounter_data.get("global", {})
        global_rankings = [
            ranking
            for ranking in valid_rankings(wcl.CharacterRankings(**global_data).rankings)
            if ranking.server.region not in ("CN", "KR")
        ][: RANKING_REGION_LIMITS["global"]]

        cn_data = encounter_data.get("cn", {})
        cn_rankings = valid_rankings(wcl.CharacterRankings(**cn_data).rankings)[: RANKING_REGION_LIMITS["cn"]]

        if cn_rankings:
            logger.info(f"[CN Data Check] First CN Player: {cn_rankings[0].name}")

        kr_data = encounter_data.get("kr", {})
        kr_rankings = valid_rankings(wcl.CharacterRankings(**kr_data).rankings)[: RANKING_REGION_LIMITS["kr"]]

        rankings = global_rankings + cn_rankings + kr_rankings
        logger.info(
            "[Ranking Quotas] global=%s cn=%s kr=%s total=%s",
            len(global_rankings),
            len(cn_rankings),
            len(kr_rankings),
            len(rankings),
        )
        self.add_new_fights(rankings)
        self.post_init()

    async def load_rankings(self) -> None:
        """Fetch the current Ranking Data"""
        query = self.get_query()
        result = await self.client.query(query)
        self.process_query_result(**result)

    def _build_report_metric_totals_query(self, report: Report) -> str:
        fight_ids = sorted({fight.fight_id for fight in report.fights if fight.fight_id})
        fight_ids_text = ", ".join(str(fight_id) for fight_id in fight_ids)
        return f"""
            reportData
            {{
                report(code: "{report.report_id}")
                {{
                    rankings(fightIDs: [{fight_ids_text}], playerMetric: {self.metric})
                }}
            }}
        """

    @staticmethod
    def _iter_report_ranking_characters(rankings_payload: dict[str, typing.Any]):
        data = rankings_payload.get("data") or []
        for fight_data in data:
            fight_id = fight_data.get("fightID")
            roles = fight_data.get("roles") or {}
            for role_data in roles.values():
                for character in (role_data or {}).get("characters") or []:
                    if character.get("id_2") or character.get("name_2"):
                        continue

                    name = character.get("name")
                    class_name = character.get("class")
                    amount = character.get("amount")
                    if not fight_id or not name or not class_name or amount is None:
                        continue

                    spec = WowSpec.get(name_slug_cap=class_name)
                    if not spec:
                        continue

                    yield fight_id, name, spec.full_name_slug, amount

    async def load_metric_totals(self) -> None:
        """Overwrite fight-summary DPS with ranking totals for the active metric."""
        if not self._should_load_buddies():
            return

        reports = [report for report in self.reports if report.report_id and report.fights]
        if not reports:
            return

        tasks = [
            self.client.query(
                self._build_report_metric_totals_query(report),
                raise_errors=False,
                region=report.region,
            )
            for report in reports
        ]
        results = await asyncio.gather(*tasks)

        metric_totals: dict[tuple[str, int, str, str], float] = {}
        for report, result in zip(reports, results):
            rankings_payload = (
                result.get("reportData", {})
                .get("report", {})
                .get("rankings", {})
            )
            for fight_id, name, spec_slug, amount in self._iter_report_ranking_characters(rankings_payload):
                key = (report.report_id, fight_id, self._normalize_name(name), spec_slug)
                metric_totals[key] = float(amount)

        applied = 0
        for report in self.reports:
            for fight in report.fights:
                for player in fight.players:
                    key = (
                        report.report_id,
                        fight.fight_id,
                        self._normalize_name(player.name),
                        player.spec_slug,
                    )
                    total = metric_totals.get(key)
                    if total is None:
                        continue

                    if player.spec_slug == self.spec_slug and player.total <= 0:
                        continue

                    if abs(player.total - total) > 0.1:
                        player.total = total
                        applied += 1

        if applied:
            logger.info(f"[Metric Totals] Applied {self.metric} totals to {applied} players.")

    ############################################################################
    # Query: Fights
    #
    def _should_load_buddies(self) -> bool:
        """Buddy rows are only useful for FF14 tank/healer comparisons."""
        return bool(self.spec and self.spec.role and self.spec.role.code in ("tank", "heal"))

    @staticmethod
    def _actor_load_key(actor: typing.Any) -> tuple[typing.Any, ...]:
        """Return a stable key so duplicate fight/player rows do not fetch twice."""
        fight = getattr(actor, "fight", None)
        report = getattr(fight, "report", None)
        report_id = getattr(report, "report_id", "")
        fight_id = getattr(fight, "fight_id", 0)

        if isinstance(actor, Player):
            return (
                "player",
                report_id,
                fight_id,
                actor.source_id,
                actor.guid,
                actor.name,
                actor.spec_slug,
            )

        if isinstance(actor, Boss):
            return ("boss", report_id, fight_id, actor.boss_slug)

        return (actor.__class__.__name__, report_id, fight_id, getattr(actor, "source_id", 0))

    async def load_actors(self) -> None:
        """Load the Casts for all missing fights."""
        # [优化] 只加载主角 (DPS > 0 的那个) 的技能数据
        actors_to_load = [p for p in self.players if p.spec_slug == self.spec_slug and p.total > 0]
        load_buddies = self._should_load_buddies()
        buddy_role_code = self.spec.role.code if load_buddies else ""

        for i, fight in enumerate(self.fights):
            if not fight.boss:
                fight.boss = Boss(boss_slug=self.boss_slug)
                fight.boss.fight = fight

            if i == 0:
                fight.boss.query_mode = fight.boss.QueryModes.ALL
            else:
                fight.boss.query_mode = fight.boss.QueryModes.PHASES

            if load_buddies:
                ranker_source_ids = {
                    p.source_id
                    for p in fight.players
                    if p.spec_slug == self.spec_slug and p.total > 0
                }
                buddy_players = [
                    p
                    for p in fight.players
                    if p.source_id not in ranker_source_ids
                    and p.spec
                    and p.spec.role
                    and p.spec.role.code == buddy_role_code
                ]
                actors_to_load.extend(buddy_players)

            actors_to_load.append(fight.boss)

        actors_to_load = [actor for actor in actors_to_load if actor and not actor.casts]
        unique_actors = []
        seen_actors = {}
        duplicate_actors = []

        for actor in actors_to_load:
            key = self._actor_load_key(actor)
            original = seen_actors.get(key)
            if original:
                duplicate_actors.append((actor, original))
                continue

            seen_actors[key] = actor
            unique_actors.append(actor)

        logger.info(f"load {len(unique_actors)} players/bosses")
        if not unique_actors:
            return

        await self.load_many(unique_actors, raise_errors=False)

        for duplicate, original in duplicate_actors:
            duplicate.casts = list(original.casts)

    ############################################################################
    # Query: Both
    #
    async def load(self, limit=50, clear_old=False) -> None:
        """Get Top Ranks for a given boss and spec."""
        logger.info(f"--- [v4-FINAL] LOADING WITH STRICT MANIFEST (No-Compromise) ---") 
        logger.info(f"{self.boss.name} vs. {self.spec.name} {self.spec.wow_class.name} START | limit={limit} | clear_old={clear_old}")

        if clear_old:
            self.reports = []

        # 1. Load Rankings (绝对真理)
        await self.load_rankings()
        self.reports = self.sort_reports(self.reports)

        # ============================================================
        # [Step A] 建立花名册 (Manifest)
        # 记录每场战斗的 "法定主角" 是谁，以及他的 "法定DPS"
        # 使用全名 (Full Name) 以避免同名不同服的冲突
        # Map Key: (report_id, fight_id) -> {name, dps}
        # ============================================================
        manifest = {}
        for report in self.reports:
            for fight in report.fights:
                if fight.players:
                    # 在 load_many 之前，列表里只有一个人，就是主角
                    p = fight.players[0]
                    key = (report.report_id, fight.fight_id)
                    manifest[key] = {
                        "name": p.name, # 使用原始全名
                        "dps": p.total
                    }
        # ============================================================

        # 2. Apply Limit
        limit = limit or -1
        self.reports = self.reports[:limit]

        # 3. Fetch Details (这一步会打乱顺序并污染数值)
        fights_missing_comp = [f for f in self.fights if len(f.players) <= 1]
        
        if fights_missing_comp:
            logger.info(f"[Fallback] Fetching Composition for {len(fights_missing_comp)} fights...")
            await self.load_many(fights_missing_comp, raise_errors=False)

            # ============================================================
            # [Step B] 执行军规 (Enforce Manifest)
            # ============================================================
            restore_count = 0
            
            for report in self.reports:
                for fight in report.fights:
                    key = (report.report_id, fight.fight_id)
                    target_info = manifest.get(key)
                    
                    if not target_info:
                        continue
                        
                    target_full_name = target_info["name"]
                    target_dps = target_info["dps"]
                    target_short_name = self._normalize_name(target_full_name)

                    # 1. 寻找唯一的 Ranker (优先全名匹配，其次短名匹配)
                    ranker_player = None
                    
                    # 尝试全名匹配 (Best)
                    for p in fight.players:
                        if p.name == target_full_name:
                            ranker_player = p
                            break
                    
                    # 尝试短名匹配 (Fallback)
                    if not ranker_player:
                        for p in fight.players:
                            if self._normalize_name(p.name) == target_short_name:
                                ranker_player = p
                                break
                    
                    # 2. 修正数值
                    if ranker_player:
                        for p in fight.players:
                            if p == ranker_player:
                                # 是主角 -> 恢复官方数值
                                if abs(p.total - target_dps) > 0.1:
                                    p.total = target_dps
                                    restore_count += 1
                            elif p.spec_slug == self.spec_slug:
                                # 是同职业的其他人 (冒充者) -> 禁言 (DPS归零)
                                p.total = 0
                    
                    # [Step C] 重新确立地位 (Re-Sort)
                    # 强制把 DPS 最高的人 (现在只能是主角了) 放到列表第一个
                    fight.players.sort(key=lambda p: p.total, reverse=True)

            logger.info(f"[DPS Fix] Enforced Manifest on {restore_count} Rankers.")
            # ============================================================

        # 4. Align buddy totals with the active ranking metric before frontend export.
        await self.load_metric_totals()

        # 5. Load Spells
        await self.load_actors()
        
        logger.info("done")

        self.updated = datetime.datetime.now(datetime.timezone.utc)
        self.dirty = False

from lorgs.models.warcraftlogs_report import Report
SpecRanking.model_rebuild()
