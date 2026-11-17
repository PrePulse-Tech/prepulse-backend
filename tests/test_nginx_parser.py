from pathlib import Path

from app.parsers.nginx import NginxAccessParser

FIXTURE = Path(__file__).parent / "fixtures" / "logs" / "nginx-access.log"


def parse_fixture():
    with FIXTURE.open() as f:
        return list(NginxAccessParser().parse(f))


def test_parses_every_line_in_fixture():
    assert len(parse_fixture()) == 77


def test_parses_fields_of_first_line():
    first = parse_fixture()[0]
    assert str(first.source_ip) == "192.0.2.24"
    assert first.status_code == 200
    assert first.message == "GET /cart"
    assert first.level == "info"
    assert first.logged_at.year == 2026


def test_finds_the_five_hundred_errors():
    errors = [line for line in parse_fixture() if line.status_code == 500]
    assert len(errors) == 12
    assert all(line.level == "error" for line in errors)


def test_finds_the_scan_traffic_from_one_ip():
    scan = [line for line in parse_fixture() if str(line.source_ip) == "198.51.100.23"]
    assert len(scan) == 25
    assert all(line.status_code in (401, 404) for line in scan)


def test_skips_lines_that_do_not_match():
    assert list(NginxAccessParser().parse(["this is not an nginx line\n"])) == []
