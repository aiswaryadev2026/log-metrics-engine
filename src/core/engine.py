from typing import List
from src.parser.log_parser import LogParser
from src.metrics.base import Metric
import logging

logger = logging.getLogger(__name__)

"""Core engine that runs the log processing pipeline."""
def run_pipeline(logfile: str, metrics: List[Metric]) -> List[Metric]:
    parser = LogParser()

    parse_error_metric = next(
        (m for m in metrics if hasattr(m, "consume_error")), None
    )

    for event in parser.parse(logfile):
        if event is None:
            if parse_error_metric:
                parse_error_metric.consume_error()
            continue

        for metric in metrics:
            metric.consume(event)

    return metrics
