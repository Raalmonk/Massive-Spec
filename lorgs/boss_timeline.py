"""Static boss timeline events for frontend encounter markers."""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Literal, Optional


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
    name_i18n: dict[str, str] = field(default_factory=dict)
    action_id: Optional[int] = None
    phase_index: Optional[int] = None
    phase_time: Optional[float] = None
    phase_name: str = ""

    def as_dict(self) -> dict:
        return asdict(self)
