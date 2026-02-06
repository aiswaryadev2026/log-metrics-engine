import statistics
from src.metrics.base import Metric
from src.model.event import LogEvent


class LatencyMetric(Metric):
    def __init__(self):
        self._latencies = []

    def consume(self, event: LogEvent) -> None:
        self._latencies.append(event.latency_ms)

    def result(self) -> dict:
        if not self._latencies:
            return {}

        sorted_latencies = sorted(self._latencies)

        p50 = statistics.median(sorted_latencies)
        p95_index = int(len(sorted_latencies) * 0.95) - 1
        p95 = sorted_latencies[max(p95_index, 0)]

        return {
            "latency_p50_ms": p50,
            "latency_p95_ms": p95,
            "latency_max_ms": max(sorted_latencies),
        }
