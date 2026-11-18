from datetime import UTC, datetime, timedelta

from app.rules.window import SlidingWindowCounter

START = datetime(2026, 11, 17, 12, 0, 0, tzinfo=UTC)


def test_counts_events_inside_the_window():
    counter = SlidingWindowCounter(timedelta(seconds=60))
    assert counter.add(START) == 1
    assert counter.add(START + timedelta(seconds=10)) == 2
    assert counter.add(START + timedelta(seconds=20)) == 3


def test_old_events_drop_out_of_the_window():
    counter = SlidingWindowCounter(timedelta(seconds=60))
    counter.add(START)
    counter.add(START + timedelta(seconds=30))
    assert counter.add(START + timedelta(seconds=61)) == 2
    assert len(counter) == 2


def test_event_exactly_one_window_old_still_counts():
    counter = SlidingWindowCounter(timedelta(seconds=60))
    counter.add(START)
    assert counter.add(START + timedelta(seconds=60)) == 2


def test_a_long_gap_resets_the_count():
    counter = SlidingWindowCounter(timedelta(seconds=60))
    counter.add(START)
    counter.add(START + timedelta(seconds=5))
    assert counter.add(START + timedelta(hours=1)) == 1
