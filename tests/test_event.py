from datetime import datetime, timezone
from src.model.event import LogEvent


def test_log_event_creation():
    event = LogEvent(
        timestamp=datetime.now(timezone.utc),
        method="GET",
        path="/api/test",
        status=200,
        latency_ms=123,
    )

    assert event.method == "GET"
    assert event.status == 200
    assert event.latency_ms == 123
