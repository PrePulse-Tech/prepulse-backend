from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.models.log_line import LogLine


def test_log_line_accepts_valid_data():
    line = LogLine(
        logged_at=datetime(2026, 11, 17, 12, 4, 3, tzinfo=UTC),
        source_ip="203.0.113.5",
        status_code=500,
        raw_line="example raw line",
    )
    assert str(line.source_ip) == "203.0.113.5"
    assert line.status_code == 500


def test_log_line_rejects_invalid_ip():
    with pytest.raises(ValidationError):
        LogLine(
            logged_at=datetime(2026, 11, 17, 12, 4, 3, tzinfo=UTC),
            source_ip="999.1.1.1",
            raw_line="example raw line",
        )
