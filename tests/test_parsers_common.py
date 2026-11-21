from pathlib import Path

import pytest

from app.parsers.auth import AuthLogParser
from app.parsers.base import LogParser
from app.parsers.mysql import MysqlErrorParser
from app.parsers.nginx import NginxAccessParser
from app.parsers.php import PhpErrorParser
from app.parsers.syslog import SyslogParser

FIXTURES = Path(__file__).parent / "fixtures" / "logs"

# (fixture file, parser, number of log entries in the fixture)
CASES = [
    ("nginx-access.log", NginxAccessParser(), 77),
    ("auth.log", AuthLogParser(year=2026), 31),
    ("php-error.log", PhpErrorParser(), 14),
    ("mysql-error.log", MysqlErrorParser(), 16),
    ("syslog.log", SyslogParser(year=2026), 19),
]
IDS = [case[0] for case in CASES]


def parse(parser: LogParser, name: str):
    with (FIXTURES / name).open() as f:
        return list(parser.parse(f))


@pytest.mark.parametrize(("name", "parser", "expected"), CASES, ids=IDS)
def test_every_fixture_entry_is_parsed(name, parser, expected):
    assert len(parse(parser, name)) == expected


@pytest.mark.parametrize(("name", "parser", "expected"), CASES, ids=IDS)
def test_timestamps_are_timezone_aware(name, parser, expected):
    assert all(line.logged_at.utcoffset() is not None for line in parse(parser, name))


@pytest.mark.parametrize(("name", "parser", "expected"), CASES, ids=IDS)
def test_every_line_keeps_its_raw_text(name, parser, expected):
    assert all(line.raw_line.strip() for line in parse(parser, name))


@pytest.mark.parametrize(("name", "parser", "expected"), CASES, ids=IDS)
def test_levels_are_known_values(name, parser, expected):
    levels = {line.level for line in parse(parser, name)}
    assert levels <= {"info", "warning", "error"}


@pytest.mark.parametrize(("name", "parser", "expected"), CASES, ids=IDS)
def test_empty_input_gives_no_lines(name, parser, expected):
    assert list(parser.parse([])) == []


@pytest.mark.parametrize(("name", "parser", "expected"), CASES, ids=IDS)
def test_blank_and_garbage_lines_are_skipped(name, parser, expected):
    assert list(parser.parse(["\n", "   \n", "garbage\n"])) == []


@pytest.mark.parametrize(("name", "parser", "expected"), CASES, ids=IDS)
def test_garbage_between_valid_lines_does_not_stop_parsing(name, parser, expected):
    with (FIXTURES / name).open() as f:
        lines = f.readlines()
    mixed = ["garbage\n", *lines[:3], "\n", "more garbage\n", *lines[3:]]
    assert len(list(parser.parse(mixed))) == expected
