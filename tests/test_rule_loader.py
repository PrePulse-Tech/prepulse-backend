import logging
from collections.abc import Iterable, Mapping
from typing import Any

from app.models.log_line import LogLine
from app.rules.base import Finding, Rule
from app.rules.loader import load_rules


class DummyRule(Rule):
    def evaluate(self, lines: Iterable[LogLine]) -> list[Finding]:
        return []


class FakeRepository:
    def __init__(self, rows: list[Mapping[str, Any]]) -> None:
        self._rows = rows

    def fetch_rules(self) -> Iterable[Mapping[str, Any]]:
        return self._rows


def row(rule_id: int, failure_type: str = "dummy", **extra: Any) -> dict[str, Any]:
    base = {
        "rule_id": rule_id,
        "name": f"Rule {rule_id}",
        "failure_type": failure_type,
        "severity": "high",
        "config": '{"threshold": 5, "window_seconds": 60}',
        "enabled": True,
    }
    return base | extra


def test_loads_an_enabled_rule_with_parsed_config():
    rules = load_rules(FakeRepository([row(1)]), {"dummy": DummyRule})
    assert len(rules) == 1
    assert isinstance(rules[0], DummyRule)
    assert rules[0].config.config == {"threshold": 5, "window_seconds": 60}
    assert rules[0].config.severity == "high"


def test_skips_disabled_rules():
    rules = load_rules(FakeRepository([row(1, enabled=False)]), {"dummy": DummyRule})
    assert rules == []


def test_skips_unknown_failure_type_and_keeps_the_rest(caplog):
    repo = FakeRepository([row(1, failure_type="unknown"), row(2)])
    with caplog.at_level(logging.WARNING):
        rules = load_rules(repo, {"dummy": DummyRule})
    assert [rule.config.rule_id for rule in rules] == [2]
    assert "unknown" in caplog.text


def test_empty_config_becomes_empty_dict():
    rules = load_rules(FakeRepository([row(1, config=None)]), {"dummy": DummyRule})
    assert rules[0].config.config == {}
