from src.metrics.base import Metric
from src.model.event import LogEvent


class ErrorRateMetric(Metric):
    def __init__(self):
        self._total = 0
        self._errors = 0

    def consume(self, event: LogEvent) -> None:
        self._total += 1
        if event.status >= 500:
            self._errors += 1

    def result(self) -> dict:
        if self._total == 0:
            rate = 0.0
        else:
            rate = (self._errors / self._total) * 100

        return {
            "error_count": self._errors,
            "error_rate_percent": round(rate, 2),
        }
