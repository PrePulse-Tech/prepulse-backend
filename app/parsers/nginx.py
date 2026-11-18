import re
from collections.abc import Iterable, Iterator
from datetime import datetime

from app.models.log_line import LogLine
from app.parsers.base import LogParser

# nginx "combined" format:
# 203.0.113.5 - - [17/Nov/2026:12:04:03 +0100] "GET /shop HTTP/1.1" 200 5123 "-" "agent"
_PATTERN = re.compile(
    r"^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "
    r'"(?P<method>\S+) (?P<path>\S+)[^"]*" '
    r"(?P<status>\d{3}) (?:\d+|-) "
    r'"[^"]*" "[^"]*"$'
)


def _level_for(status: int) -> str:
    if status >= 500:
        return "error"
    if status >= 400:
        return "warning"
    return "info"


class NginxAccessParser(LogParser):
    """Parses nginx access logs in the combined format."""

    def parse(self, lines: Iterable[str]) -> Iterator[LogLine]:
        for line in lines:
            raw = line.rstrip("\n")
            match = _PATTERN.match(raw)
            if match is None:
                continue
            status = int(match["status"])
            yield LogLine(
                logged_at=datetime.strptime(match["time"], "%d/%b/%Y:%H:%M:%S %z"),
                level=_level_for(status),
                message=f"{match['method']} {match['path']}",
                source_ip=match["ip"],
                status_code=status,
                raw_line=raw,
            )
