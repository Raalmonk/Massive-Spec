#!/usr/bin/env python
"""Load a Report given by an URL"""

# IMPORT STANDARD LIBRARIES
from urllib.parse import urlparse, parse_qs
import argparse
import asyncio
import dotenv
import re

import pydantic

dotenv.load_dotenv()  # pylint: disable=wrong-import-position

# IMPORT LOCAL LIBRARIES
from lorgs import data  # pylint: disable=unused-import
from lorgs.models.warcraftlogs_user_report import UserReport

from lorgs.data.season import CURRENT_SEASON


class WarcraftReport(pydantic.BaseModel):
    """Small Helper Class to Hold Report Information."""

    report_id: str
    fight_ids: list[int] = []
    player_ids: list[int] = []

    @classmethod
    def from_url(cls, url: str):
        report_match = re.search(r"reports/(\w{16})", url)
        report_id = report_match.group(1) if report_match else ""

        query_params = parse_qs(urlparse(url).query)
        fight_ids = [int(v) for v in query_params.get("fight", [-1])]
        player_ids = [int(v) for v in query_params.get("source", [-1])]

        return cls(
            report_id=report_id,
            fight_ids=fight_ids,
            player_ids=player_ids,
        )

    def as_lorrgs_url(self) -> str:

        def to_str(l: list, j: str = ".") -> str:
            return j.join([str(i) for i in l])

        fight_ids_str = to_str(self.fight_ids)
        player_ids_str = to_str(self.player_ids)
        return f"http://localhost:9001/user_report/{self.report_id}?fight={fight_ids_str}&player={player_ids_str}"

    async def load(self) -> None:
        print(f"Loading Report: {self.report_id}")

        # 1. Instantiate directly (Bypass DB lookup)
        user_report = UserReport(report_id=self.report_id)

        # 2. Load Master Data
        await user_report.load()

        # 3. Load Fights
        await user_report.load_fights(fight_ids=self.fight_ids, player_ids=self.player_ids)

        # 4. Print results instead of saving
        # user_report.save() # <--- Commented out to avoid AWS connection

        print("\n" + "="*30)
        print(f"Report: {user_report.title}")
        for fight in user_report.fights:
            print(f"Fight: {fight.boss.raid_boss.name if fight.boss else 'Unknown'} (ID: {fight.fight_id})")
            for player in fight.players:
                print(f" - Player: {player.name} ({player.spec_slug}) | Casts: {len(player.casts)}")
        print("="*30 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load a Warcraft Logs report.")
    parser.add_argument("url", nargs="?", type=str, help="Full Warcraft Logs report URL")
    parser.add_argument("--report", type=str, help="Report ID")
    parser.add_argument("--fight", type=int, nargs="+", help="Fight IDs", default=[-1])
    parser.add_argument("--source", type=int, nargs="+", help="Source (Player) IDs", default=[-1])

    args = parser.parse_args()

    if args.url:
        report = WarcraftReport.from_url(args.url)
    elif args.report:
        report = WarcraftReport(
            report_id=args.report,
            fight_ids=args.fight,
            player_ids=args.source,
        )
    else:
        parser.error("Either --url or --report must be provided.")

    print("--- Loading ----")
    print(report)
    asyncio.run(report.load())
