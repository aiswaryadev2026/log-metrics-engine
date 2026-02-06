from datetime import datetime
from src.metrics.request_count import RequestCountMetric
from src.model.event import LogEvent


def test_request_count_metric():
    metric = RequestCountMetric()

    event = LogEvent(
        timestamp=datetime.utcnow(),
        method="GET",
        path="/",
        status=200,
        latency_ms=10,
    )

    metric.consume(event)
    metric.consume(event)

    result = metric.result()
    assert result["request_count"] == 2
