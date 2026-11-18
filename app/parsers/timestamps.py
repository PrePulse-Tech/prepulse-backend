import re
from datetime import UTC, datetime, tzinfo

_MONTHS = {
    name: number
    for number, name in enumerate(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        start=1,
    )
}

_SYSLOG_TIME = re.compile(
    r"^(?P<month>\w{3}) +(?P<day>\d{1,2}) (?P<h>\d\d):(?P<m>\d\d):(?P<s>\d\d)$"
)


def parse_syslog_time(text: str, year: int, tz: tzinfo = UTC) -> datetime:
    """Turn a syslog timestamp like 'Nov 17 12:04:03' into a timezone-aware datetime.

    Syslog timestamps have no year and no timezone, so the caller has to supply them.
    """
    match = _SYSLOG_TIME.match(text)
    if match is None:
        raise ValueError(f"Not a syslog timestamp: {text!r}")
    return datetime(
        year,
        _MONTHS[match["month"]],
        int(match["day"]),
        int(match["h"]),
        int(match["m"]),
        int(match["s"]),
        tzinfo=tz,
    )
