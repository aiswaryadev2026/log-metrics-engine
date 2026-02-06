from src.metrics.base import Metric
from src.model.event import LogEvent


class RequestCountMetric(Metric):
    def __init__(self):
        self._count = 0

    def consume(self, event: LogEvent) -> None:
        self._count += 1

    def result(self) -> dict:
        return {"request_count": self._count}
