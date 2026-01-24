import unittest
from unittest import mock
import datetime
from lorgs.models.warcraftlogs_ranking import SpecRanking
from lorgs.clients import wcl
from lorgs.clients.wcl.models.character_ranking import CharacterRankingReportFightData

# Rebuild models
from lorgs.models.warcraftlogs_fight import Fight
from lorgs.models.warcraftlogs_report import Report
Fight.model_rebuild()
Report.model_rebuild()

class TestSpecRankingPartners(unittest.TestCase):
    def setUp(self):
        self.spec_ranking = SpecRanking(spec_slug="healer-spec", boss_slug="boss", metric="dps")

        # Mock Spec Property
        self.spec_ranking_spec_mock = mock.MagicMock()
        self.spec_ranking_spec_mock.role.code = "heal"
        self.spec_ranking_spec_mock.full_name_slug = "healer-spec"

        # We need to mock the property 'spec' on the instance or class
        # Since 'spec' is a property that calls WowSpec.get, we can just mock WowSpec.get

        self.spec_patch = mock.patch("lorgs.models.wow_spec.WowSpec.get")
        self.spec_mock = self.spec_patch.start()

        def get_spec(name_slug_cap=None, wow_class__name_slug_cap=None, **kwargs):
            m = mock.MagicMock()
            if name_slug_cap == "HealerSpec":
                m.role.code = "heal"
                m.full_name_slug = "healer-spec"
            elif name_slug_cap == "TankSpec":
                m.role.code = "tank"
                m.full_name_slug = "tank-spec"
            elif name_slug_cap == "OtherHealerSpec":
                m.role.code = "heal"
                m.full_name_slug = "other-healer-spec"
            else:
                 m.role.code = "dps"
                 m.full_name_slug = "dps-spec"
            return m

        self.spec_mock.side_effect = get_spec

        # We also need to mock self.spec_ranking.spec calls inside the class methods if any
        # But specifically add_new_fight uses self.spec.role.code.
        # Since self.spec calls WowSpec.get(full_name_slug=self.spec_slug), let's ensure that returns our main spec

        # Update side_effect to handle full_name_slug lookup too
        def get_spec_wrapper(full_name_slug=None, name_slug_cap=None, wow_class__name_slug_cap=None, **kwargs):
            if full_name_slug == "healer-spec":
                return self.spec_ranking_spec_mock

            # call original side effect logic
            return get_spec(name_slug_cap, wow_class__name_slug_cap)

        self.spec_mock.side_effect = get_spec_wrapper

    def tearDown(self):
        self.spec_patch.stop()

    def test_add_new_fight_filters_partners(self):
        ranking_data = wcl.CharacterRanking.model_validate({
            "name": "MainHealer",
            "class": "HealerClass",
            "spec": "HealerSpec",
            "amount": 1000,
            "duration": 10000,
            "startTime": datetime.datetime.now(),
            "report": {
                "code": "TEST",
                "fightID": 1,
                "startTime": datetime.datetime.now()
            },
            "combatantInfo": [
                {"name": "MainHealer", "spec": "HealerSpec", "type": "HealerClass", "id": 1},
                {"name": "PartnerHealer", "spec": "OtherHealerSpec", "type": "HealerClass", "id": 2}, # Should be added (Same Role)
                {"name": "TankPartner", "spec": "TankSpec", "type": "TankClass", "id": 3},       # Should be SKIPPED (Different Role)
            ]
        })

        self.spec_ranking.add_new_fight(ranking_data)

        report = self.spec_ranking.reports[0]
        fight = report.fights[0]

        # Expecting 3 players: MainHealer + PartnerHealer + TankPartner
        self.assertEqual(len(fight.players), 3)

        player_names = [p.name for p in fight.players]
        self.assertIn("MainHealer", player_names)
        self.assertIn("PartnerHealer", player_names)
        self.assertIn("TankPartner", player_names)

        # Check composition
        expected_composition = ["healer-spec", "other-healer-spec", "tank-spec"]
        self.assertEqual(fight.composition, expected_composition)
