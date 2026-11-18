from collections import deque
from datetime import datetime, timedelta


class SlidingWindowCounter:
    """Counts events that happened within the last `window` of time.

    Events must be added in time order, which is how log lines arrive.
    """

    def __init__(self, window: timedelta) -> None:
        self._window = window
        self._events: deque[datetime] = deque()

    def add(self, at: datetime) -> int:
        """Register an event and return how many events are inside the window."""
        self._events.append(at)
        while self._events and at - self._events[0] > self._window:
            self._events.popleft()
        return len(self._events)

    def __len__(self) -> int:
        return len(self._events)
