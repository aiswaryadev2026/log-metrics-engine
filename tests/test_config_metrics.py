from src.metrics.registry import METRIC_REGISTRY


def test_metric_registry_contains_expected_metrics():
    assert "request_count" in METRIC_REGISTRY
    assert "error_rate" in METRIC_REGISTRY
    assert "latency" in METRIC_REGISTRY
