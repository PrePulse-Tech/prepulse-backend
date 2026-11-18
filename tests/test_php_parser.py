from pathlib import Path

from app.parsers.php import PhpErrorParser

FIXTURE = Path(__file__).parent / "fixtures" / "logs" / "php-error.log"


def parse_fixture():
    with FIXTURE.open() as f:
        return list(PhpErrorParser().parse(f))


def test_each_entry_becomes_one_log_line():
    assert len(parse_fixture()) == 14


def test_levels_are_derived_from_php_error_kind():
    lines = parse_fixture()
    assert len([line for line in lines if line.level == "error"]) == 9
    assert len([line for line in lines if line.level == "warning"]) == 5


def test_stack_trace_is_kept_with_its_entry():
    fatal = [line for line in parse_fixture() if "calculate_vat" in line.message]
    assert len(fatal) == 8
    for line in fatal:
        assert "Stack trace:" in line.raw_line
        assert "thrown in" in line.raw_line
        assert "Stack trace" not in line.message


def test_timezone_comes_from_the_log_line():
    first = parse_fixture()[0]
    assert first.logged_at.utcoffset() is not None
    assert first.logged_at.year == 2026


def test_skips_lines_before_the_first_entry():
    assert list(PhpErrorParser().parse(["#0 {main}\n", "garbage\n"])) == []
