from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LogEvent:
    """
    Core domain object representing a single log entry.
    """
    timestamp: datetime
    method: str
    path: str
    status: int
    latency_ms: int