from collections.abc import Iterable
from datetime import UTC, datetime, timedelta

from app.models.log_line import LogLine
from app.rules.base import Finding, Rule, RuleConfig
from app.rules.window import SlidingWindowCounter

START = datetime(2026, 11, 17, 12, 0, 0, tzinfo=UTC)


class ErrorBurstRule(Rule):
    """Dummy rule: finding when `threshold` errors happen within `window_seconds`."""

    def evaluate(self, lines: Iterable[LogLine]) -> list[Finding]:
        window = timedelta(seconds=self.config.config["window_seconds"])
        threshold = self.config.config["threshold"]
        counter = SlidingWindowCounter(window)
        recent: list[LogLine] = []
        for line in lines:
            if line.level != "error":
                continue
            counter.add(line.logged_at)
            recent.append(line)
            recent = recent[-len(counter) :]
            if len(counter) >= threshold:
                return [
                    Finding(
                        rule_id=self.config.rule_id,
                        severity=self.config.severity,
                        first_seen=recent[0].logged_at,
                        last_seen=recent[-1].logged_at,
                        lines=recent,
                    )
                ]
        return []


def make_rule() -> ErrorBurstRule:
    return ErrorBurstRule(
        RuleConfig(
            rule_id=1,
            name="Error burst",
            failure_type="error_burst",
            severity="high",
            config={"threshold": 3, "window_seconds": 60},
        )
    )


def make_line(seconds: int, level: str = "error") -> LogLine:
    return LogLine(logged_at=START + timedelta(seconds=seconds), level=level, raw_line="x")


def test_rule_reports_a_finding_when_threshold_is_reached():
    findings = make_rule().evaluate([make_line(0), make_line(10), make_line(20)])
    assert len(findings) == 1
    assert findings[0].event_count == 3
    assert findings[0].severity == "high"
    assert findings[0].first_seen == START
    assert findings[0].last_seen == START + timedelta(seconds=20)


def test_rule_reports_nothing_when_errors_are_spread_out():
    lines = [make_line(0), make_line(100), make_line(200), make_line(300)]
    assert make_rule().evaluate(lines) == []


def test_rule_ignores_lines_that_are_not_errors():
    lines = [make_line(0, "info"), make_line(10, "warning"), make_line(20, "info")]
    assert make_rule().evaluate(lines) == []
