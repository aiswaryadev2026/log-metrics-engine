import json
from typing import List
from src.metrics.base import Metric


class JsonReportFormatter:
    """
    Formats metrics into a single JSON report.
    """

    def format(self, metrics: List[Metric]) -> str:
        report = {}

        for metric in metrics:
            report.update(metric.result())

        return json.dumps(report, indent=2, sort_keys=True)
