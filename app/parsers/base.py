from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator

from app.models.log_line import LogLine


class LogParser(ABC):
    """Turns raw log text into LogLine objects.

    One subclass per log format. parse() takes all lines at once, so formats
    where one entry spans several lines (like PHP stack traces) can be handled
    the same way as single-line formats.
    """

    @abstractmethod
    def parse(self, lines: Iterable[str]) -> Iterator[LogLine]:
        """Yield one LogLine per log entry. Lines that do not match are skipped."""
