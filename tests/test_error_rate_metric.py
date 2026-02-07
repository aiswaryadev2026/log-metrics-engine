from datetime import datetime, timezone
from src.metrics.error_rate import ErrorRateMetric
from src.model.event import LogEvent


def test_error_rate_metric():
    metric = ErrorRateMetric()

    ok_event = LogEvent(
        timestamp=datetime.now(timezone.utc),
        method="GET",
        path="/",
        status=200,
        latency_ms=10,
    )

    error_event = LogEvent(
        timestamp=datetime.now(timezone.utc),
        method="GET",
        path="/",
        status=500,
        latency_ms=20,
    )

    metric.consume(ok_event)
    metric.consume(error_event)

    result = metric.result()

    assert result["error_count"] == 1
    assert result["error_rate_percent"] == 50.0
