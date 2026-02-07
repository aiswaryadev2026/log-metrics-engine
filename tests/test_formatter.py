import json
from src.report.formatter import JsonReportFormatter
from src.metrics.request_count import RequestCountMetric


def test_json_report_formatter():
    metric = RequestCountMetric()
    metric._count = 5  # controlled test state

    formatter = JsonReportFormatter()
    output = formatter.format([metric])

    data = json.loads(output)
    assert data["request_count"] == 5
