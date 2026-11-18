from abc import ABC, abstractmethod
from collections.abc import Iterable
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.log_line import LogLine


class RuleConfig(BaseModel):
    """One row of the detection_rule table.

    `config` holds the rule's own settings (thresholds, time windows and so on).
    """

    rule_id: int
    name: str
    failure_type: str
    severity: str
    config: dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True


class Finding(BaseModel):
    """What a rule reports when it detects something. Becomes an incident later."""

    rule_id: int
    severity: str
    first_seen: datetime
    last_seen: datetime
    lines: list[LogLine]

    @property
    def event_count(self) -> int:
        return len(self.lines)


class Rule(ABC):
    """Base class for all detection rules.

    A rule gets its settings from a RuleConfig and looks at parsed log lines.
    """

    def __init__(self, config: RuleConfig) -> None:
        self.config = config

    @abstractmethod
    def evaluate(self, lines: Iterable[LogLine]) -> list[Finding]:
        """Return a Finding for each incident the rule detects in the lines."""
