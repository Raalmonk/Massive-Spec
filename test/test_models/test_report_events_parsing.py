import pytest
from lorgs.clients.wcl.models.report_events import ReportEvent

def test_report_event_parsing_with_abilityID():
    data = {
        "timestamp": 123456,
        "type": "cast",
        "sourceID": 1,
        "targetID": 2,
        "abilityID": 100,
        "fight": 1
    }
    event = ReportEvent(**data)
    assert event.abilityGameID == 100
