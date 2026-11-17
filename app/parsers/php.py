import re
from collections.abc import Iterable, Iterator
from datetime import datetime
from zoneinfo import ZoneInfo

from app.models.log_line import LogLine
from app.parsers.base import LogParser

# [17-Nov-2026 12:04:08 Europe/Copenhagen] PHP Fatal error:  Uncaught Error: ...
# Lines that do not start like this (Stack trace:, #0 {main}, thrown in ...) belong
# to the entry above them.
_START = re.compile(
    r"^\[(?P<time>\d{2}-\w{3}-\d{4} \d{2}:\d{2}:\d{2}) (?P<tz>[^\]]+)\] "
    r"PHP (?P<kind>[^:]+):  (?P<message>.*)$"
)


def _level_for(kind: str) -> str:
    kind = kind.lower()
    if kind in ("fatal error", "parse error"):
        return "error"
    if kind == "warning":
        return "warning"
    return "info"


def _build(start: re.Match[str], raw_lines: list[str]) -> LogLine:
    logged_at = datetime.strptime(start["time"], "%d-%b-%Y %H:%M:%S").replace(
        tzinfo=ZoneInfo(start["tz"])
    )
    return LogLine(
        logged_at=logged_at,
        level=_level_for(start["kind"]),
        message=start["message"],
        raw_line="\n".join(raw_lines),
    )


class PhpErrorParser(LogParser):
    """Parses the PHP error log, including entries that span several lines."""

    def parse(self, lines: Iterable[str]) -> Iterator[LogLine]:
        current: tuple[re.Match[str], list[str]] | None = None
        for line in lines:
            raw = line.rstrip("\n")
            start = _START.match(raw)
            if start is not None:
                if current is not None:
                    yield _build(*current)
                current = (start, [raw])
            elif current is not None and raw.strip():
                current[1].append(raw)
        if current is not None:
            yield _build(*current)
