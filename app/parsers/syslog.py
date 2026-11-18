import re
from collections.abc import Iterable, Iterator
from datetime import UTC, tzinfo

from app.models.log_line import LogLine
from app.parsers.base import LogParser
from app.parsers.timestamps import parse_syslog_time

# Nov 17 12:22:02 web01 systemd[1]: php8.2-fpm.service: Main process exited
_LINE = re.compile(
    r"^(?P<time>\w{3} +\d{1,2} [\d:]{8}) \S+ "
    r"(?P<process>[^:\[\s]+)(?:\[\d+\])?: (?P<message>.*)$"
)

_ERROR_HINTS = ("failed", "killed", "out of memory", "repeated too quickly")


def _level_for(message: str) -> str:
    text = message.lower()
    if any(hint in text for hint in _ERROR_HINTS):
        return "error"
    if "restart" in text:
        return "warning"
    return "info"


class SyslogParser(LogParser):
    """Parses general syslog lines (systemd, kernel and so on).

    Like auth.log, the timestamps have no year and no timezone.
    """

    def __init__(self, year: int, tz: tzinfo = UTC) -> None:
        self._year = year
        self._tz = tz

    def parse(self, lines: Iterable[str]) -> Iterator[LogLine]:
        for line in lines:
            raw = line.rstrip("\n")
            match = _LINE.match(raw)
            if match is None:
                continue
            yield LogLine(
                logged_at=parse_syslog_time(match["time"], self._year, self._tz),
                level=_level_for(match["message"]),
                message=f"{match['process']}: {match['message']}",
                raw_line=raw,
            )
