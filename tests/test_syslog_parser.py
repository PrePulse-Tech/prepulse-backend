from pathlib import Path

from app.parsers.syslog import SyslogParser

FIXTURE = Path(__file__).parent / "fixtures" / "logs" / "syslog.log"


def parse_fixture():
    with FIXTURE.open() as f:
        return list(SyslogParser(year=2026).parse(f))


def test_parses_every_line_in_fixture():
    assert len(parse_fixture()) == 19


def test_out_of_memory_kill_is_an_error():
    oom = [line for line in parse_fixture() if "Out of memory" in line.message]
    assert len(oom) == 1
    assert oom[0].level == "error"


def test_finds_the_restart_attempts():
    restarts = [line for line in parse_fixture() if "Scheduled restart job" in line.message]
    assert len(restarts) == 4
    assert all(line.level == "warning" for line in restarts)


def test_skips_lines_that_do_not_match():
    assert list(SyslogParser(year=2026).parse(["not a syslog line\n"])) == []
