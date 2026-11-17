import re
from collections.abc import Iterable, Iterator
from datetime import UTC, tzinfo

from app.models.log_line import LogLine
from app.parsers.base import LogParser
from app.parsers.timestamps import parse_syslog_time

# Nov 17 12:12:03 web01 sshd[2203]: Failed password for root from 203.0.113.5 port 4927
_LINE = re.compile(r"^(?P<time>\w{3} +\d{1,2} [\d:]{8}) \S+ sshd\[\d+\]: (?P<message>.*)$")

# The three kinds of sshd messages we care about. All of them carry user and IP.
_EVENT = re.compile(
    r"^(?:Failed \w+ for (?:invalid user )?|Invalid user |Accepted \w+ for )"
    r"(?P<user>\S+) from (?P<ip>\S+) port \d+"
)


class AuthLogParser(LogParser):
    """Parses OpenSSH lines from auth.log.

    auth.log timestamps have no year and no timezone, so both are given when the
    parser is created.
    """

    def __init__(self, year: int, tz: tzinfo = UTC) -> None:
        self._year = year
        self._tz = tz

    def parse(self, lines: Iterable[str]) -> Iterator[LogLine]:
        for line in lines:
            raw = line.rstrip("\n")
            outer = _LINE.match(raw)
            if outer is None:
                continue
            event = _EVENT.match(outer["message"])
            if event is None:
                continue
            yield LogLine(
                logged_at=parse_syslog_time(outer["time"], self._year, self._tz),
                level="info" if outer["message"].startswith("Accepted") else "warning",
                message=outer["message"],
                source_ip=event["ip"],
                username=event["user"],
                raw_line=raw,
            )
