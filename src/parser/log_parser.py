from datetime import datetime
from typing import Iterator

from src.model.event import LogEvent
import logging

logger = logging.getLogger(__name__)


class LogParser:
    """
    Streaming log parser that converts raw log lines into LogEvent objects.
    """

    def parse(self, file_path: str) -> Iterator[LogEvent]:
        """
        Parse a log file line by line and yield LogEvent objects.
        """
        with open(file_path, "r") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                yield self._parse_line(line, line_number)

    def _parse_line(self, line: str, line_number: int) -> LogEvent:
        """
        Parse a single log line into a LogEvent.
        Expected format:
        <timestamp> <method> <path> <status> <latency_ms>
        """
        try:
            parts = line.split()
            return LogEvent(
                timestamp=self._parse_timestamp(parts[0]),
                method=parts[1],
                path=parts[2],
                status=int(parts[3]),
                latency_ms=int(parts[4]),
            )
        except (IndexError, ValueError) as exc:
            raise ValueError(
                f"Failed to parse line {line_number}: {line}"
            ) from exc

    @staticmethod
    def _parse_timestamp(value: str) -> datetime:
        # Convert ISO-8601 Zulu time to Python datetime
        return datetime.fromisoformat(value.replace("Z", "+00:00"))