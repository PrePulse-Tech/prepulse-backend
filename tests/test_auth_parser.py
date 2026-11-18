from pathlib import Path

from app.parsers.auth import AuthLogParser

FIXTURE = Path(__file__).parent / "fixtures" / "logs" / "auth.log"


def parse_fixture():
    with FIXTURE.open() as f:
        return list(AuthLogParser(year=2026).parse(f))


def test_parses_every_line_in_fixture():
    assert len(parse_fixture()) == 31


def test_finds_the_failed_logins_from_one_ip():
    failed = [
        line
        for line in parse_fixture()
        if line.message.startswith("Failed password") and str(line.source_ip) == "203.0.113.5"
    ]
    assert len(failed) == 24
    assert all(line.level == "warning" for line in failed)


def test_successful_logins_are_info():
    accepted = [line for line in parse_fixture() if line.message.startswith("Accepted")]
    assert len(accepted) == 2
    assert all(line.level == "info" and line.username == "deploy" for line in accepted)


def test_username_is_found_for_invalid_users():
    ubuntu = [line for line in parse_fixture() if line.username == "ubuntu"]
    assert len(ubuntu) == 6


def test_year_and_timezone_come_from_the_parser():
    first = parse_fixture()[0]
    assert (first.logged_at.year, first.logged_at.month, first.logged_at.day) == (
        2026,
        11,
        17,
    )
    assert first.logged_at.tzinfo is not None


def test_skips_lines_that_do_not_match():
    assert list(AuthLogParser(year=2026).parse(["not an auth line\n"])) == []
