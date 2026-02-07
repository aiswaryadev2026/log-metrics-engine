from datetime import datetime, timezone
from src.metrics.latency import LatencyMetric
from src.model.event import LogEvent


def test_latency_metric_percentiles():
    metric = LatencyMetric()

    latencies = [100, 200, 300, 400, 500]

    for latency in latencies:
        metric.consume(
            LogEvent(
                timestamp=datetime.now(timezone.utc),
                method="GET",
                path="/",
                status=200,
                latency_ms=latency,
            )
        )

    result = metric.result()

    assert result["latency_p50_ms"] == 300
    assert result["latency_p95_ms"] >= 400
    assert result["latency_max_ms"] == 500
