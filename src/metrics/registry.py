from src.metrics.request_count import RequestCountMetric
from src.metrics.error_rate import ErrorRateMetric
from src.metrics.latency import LatencyMetric

METRIC_REGISTRY = {
    "request_count": RequestCountMetric,
    "error_rate": ErrorRateMetric,
    "latency": LatencyMetric,
}
