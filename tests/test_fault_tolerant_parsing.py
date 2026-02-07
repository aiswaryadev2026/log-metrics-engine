from src.core.engine import run_pipeline
from src.metrics.parse_errors import ParseErrorMetric
from src.metrics.request_count import RequestCountMetric
import tempfile


def test_fault_tolerant_parsing():
    content = """2024-09-10T10:15:30Z GET /api/orders 200 123
INVALID LINE
2024-09-10T10:15:32Z GET /api/users 200 98
"""

    with tempfile.NamedTemporaryFile(mode="w+") as f:
        f.write(content)
        f.seek(0)

        metrics = [
            RequestCountMetric(),
            ParseErrorMetric(),
        ]

        run_pipeline(f.name, metrics)

        results = {k: v for m in metrics for k, v in m.result().items()}

        assert results["request_count"] == 2
        assert results["parse_errors"] == 1
