from pathlib import Path

from app.parsers.mysql import MysqlErrorParser

FIXTURE = Path(__file__).parent / "fixtures" / "logs" / "mysql-error.log"


def parse_fixture():
    with FIXTURE.open() as f:
        return list(MysqlErrorParser().parse(f))


def test_parses_every_line_in_fixture():
    assert len(parse_fixture()) == 16


def test_levels_are_lowercased():
    assert {line.level for line in parse_fixture()} == {"error", "warning"}


def test_finds_too_many_connections_and_deadlocks():
    lines = parse_fixture()
    assert len([line for line in lines if "Too many connections" in line.message]) == 7
    assert len([line for line in lines if "Deadlock" in line.message]) == 2


def test_aborted_connection_has_user_and_ip():
    aborted = [line for line in parse_fixture() if line.message.startswith("Aborted")]
    assert len(aborted) == 4
    assert all(line.username == "app" for line in aborted)
    assert all(str(line.source_ip) == "192.0.2.10" for line in aborted)


def test_keeps_timezone_from_the_log():
    first = parse_fixture()[0]
    assert first.logged_at.utcoffset() is not None


def test_skips_lines_that_do_not_match():
    assert list(MysqlErrorParser().parse(["not a mysql line\n"])) == []
