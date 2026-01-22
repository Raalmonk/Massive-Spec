# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel, Field, AliasChoices


class ReportEvent(BaseModel):
    """Represents a single event that occurs in the fight."""

    timestamp: int = 0
    """Timestamp of the Event (Milliseconds relative to the Report Start)."""

    type: str = "cast"
    """The type of Event. """

    sourceID: int = 0

    targetID: int = 0

    abilityGameID: int = Field(0, validation_alias=AliasChoices("abilityID", "abilityGameID"))

    fight: int = 0
