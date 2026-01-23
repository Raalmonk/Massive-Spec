import unittest
from unittest.mock import Mock
import arrow
import datetime

from lorgs.models.warcraftlogs_report import Report
from lorgs.clients import wcl

# Import a class to ensure data is loaded for Player creation
from lorgs.data.classes import astrologian


class TestReport(unittest.TestCase):

    def setUp(self) -> None:
        self.report = Report(report_id="REPORT_ID")

    def test__get_query(self):

        query = self.report.get_query()
        assert "REPORT_ID" in query

    def test__process_query_result__title(self):

        query_result = {"report": {"title": "new title"}}

        assert self.report.title != "new title"
        self.report.process_query_result(**query_result)
        assert self.report.title == "new title"

    def test__process_query_result__start_time(self):

        query_result = {"report": {"startTime": 123456}}

        assert self.report.start_time == datetime.datetime.min
        self.report.process_query_result(**query_result)
        assert self.report.start_time == arrow.get(123456)

    def test__process_query_result__region(self):
        query_result = {"report": {"region": {"slug": "cn"}}}

        self.report.process_query_result(**query_result)
        assert self.report.region == "CN"

    def test__process_query_result__zone_id_valid(self):

        query_result = {"report": {"zone": {"id": 42}}}

        self.report.process_query_result(**query_result)
        assert self.report.zone_id == 42

    def test__process_query_result__zone_id_invalid(self):

        query_result = {"report": {}} # Minimal report to satisfy ReportData validator

        self.report.process_query_result(**query_result)
        assert self.report.zone_id == -1

    ############################################################################
    #
    # _process_master_data
    #

    def test__process_master_data__clears_data(self):
        # We need to simulate that players is not empty initially
        self.report.players = ["some", "data"]

        mock_data = Mock()
        mock_data.actors = []
        self.report.process_master_data(mock_data)
        assert self.report.players == []

    ############################################################################
    #
    # add player
    #

    def test__add_player__create_player(self):

        actor_data = wcl.ReportActor(
            id=32,
            name="PlayerName",
            icon="Astrologian-Astrologian",
            type="Player",
            subType="Astrologian",
            gameID=100
        )

        self.report.add_player(actor_data)

        assert len(self.report.players) == 1
        player = self.report.players[0]
        assert player.source_id == 32
        assert player.name == "PlayerName"
        assert player.spec_slug == "astrologian-astrologian"
        assert player.class_slug == "astrologian"

    def test__add_player__unknown_spec(self):

        actor_data = wcl.ReportActor(
            id=5,
            name="HunterName",
            icon="Hunter",
            type="Player",
            subType="Hunter",
            gameID=101
        )

        self.report.add_player(actor_data)

        # Hunter is not loaded, so player.class_ will be None
        # add_player skips players with unknown class
        assert len(self.report.players) == 0

    ############################################################################
    #
    # process_report_fights
    #

    def test__add_fight__skip_trash_fight(self):

        fight_data = wcl.ReportFight(
            id=1,
            startTime=0,
            endTime=100,
            encounterID=0 # trash
        )
        self.report.add_fight(fight_data)

        assert not self.report.fights

    def test__add_fight__basic(self):
        # Set a valid start time so we can check timestamps
        self.report.start_time = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)

        fight_data = wcl.ReportFight(
            id=10,
            encounterID=2407,
            fightPercentage=70.99,
            kill=False,
            startTime=400000,
            endTime=500000
        )
        self.report.add_fight(fight_data)

        assert len(self.report.fights) == 1
        fight = self.report.fights[0]

        assert fight.percent == 70.99
        assert fight.kill == False
        assert fight.duration == 100001

        expected_start = self.report.start_time.timestamp() + 400
        assert fight.start_time.timestamp() == expected_start
