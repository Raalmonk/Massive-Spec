"""Static boss timeline events for frontend encounter markers."""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from typing import Literal


BossTimelineType = Literal["mech", "tb", "aoe"]


@dataclass(frozen=True)
class BossTimelineEvent:
    id: str
    name: str
    time: float
    duration: float = 0
    type: BossTimelineType = "mech"
    color: str = ""
    icon: str = ""

    def as_dict(self) -> dict:
        return asdict(self)
