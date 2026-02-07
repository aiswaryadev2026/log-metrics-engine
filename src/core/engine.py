from typing import List
from src.parser.log_parser import LogParser
from src.metrics.base import Metric
import logging

logger = logging.getLogger(__name__)


def run_pipeline(logfile: str, metrics: List[Metric]) -> List[Metric]:
    """
    Run the log analysis pipeline.

    Args:
        logfile: Path to the log file
        metrics: List of metric instances

    Returns:
        List of metrics after consuming all events
    """
    parser = LogParser()

    for event in parser.parse(logfile):
        for metric in metrics:
            metric.consume(event)

    return metrics
