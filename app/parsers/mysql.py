import re
from collections.abc import Iterable, Iterator
from datetime import datetime
from ipaddress import ip_address

from app.models.log_line import LogLine
from app.parsers.base import LogParser

# 2026-11-17T12:16:24.18+01:00 27 [ERROR] [MY-010584] [Server] Too many connections
_LINE = re.compile(
    r"^(?P<time>\S+) \d+ \[(?P<level>\w+)\] \[MY-\d+\] \[\w+\] "
    r"(?P<message>.*)$"
)
_USER = re.compile(r"user: '(?P<user>[^']*)'")
_HOST = re.compile(r"host: '(?P<host>[^']*)'")


def _ip_or_none(text: str) -> str | None:
    """Return text if it is an IP address. MySQL can also log a hostname here."""
    try:
        ip_address(text)
    except ValueError:
        return None
    return text


class MysqlErrorParser(LogParser):
    """Parses the MySQL 8 error log."""

    def parse(self, lines: Iterable[str]) -> Iterator[LogLine]:
        for line in lines:
            raw = line.rstrip("\n")
            match = _LINE.match(raw)
            if match is None:
                continue
            message = match["message"]
            user = _USER.search(message)
            host = _HOST.search(message)
            yield LogLine(
                logged_at=datetime.fromisoformat(match["time"]),
                level=match["level"].lower(),
                message=message,
                source_ip=_ip_or_none(host["host"]) if host else None,
                username=user["user"] if user else None,
                raw_line=raw,
            )
