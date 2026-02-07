import argparse

from src.parser.log_parser import LogParser
from src.metrics.request_count import RequestCountMetric
from src.metrics.error_rate import ErrorRateMetric
from src.metrics.latency import LatencyMetric
from src.report.formatter import JsonReportFormatter
from src.config.loader import load_config
from src.metrics.registry import METRIC_REGISTRY
import logging


logging.basicConfig(level=logging.INFO)



def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Streaming log analyzer and metrics generator"
    )
    parser.add_argument(
        "logfile",
        help="Path to the log file to analyze",
    )
    parser.add_argument(
        "--format",
        choices=["json"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
    "--config",
    required=False,
    help="Path to metrics configuration file (YAML)",
)
    return parser


def main():
    arg_parser = build_arg_parser()
    args = arg_parser.parse_args()

    parser = LogParser()

    if args.config:
        config = load_config(args.config)
        metric_names = config.get("metrics", [])
    else:
        metric_names = ["request_count", "error_rate", "latency"]

    metrics = []
    for name in metric_names:
        metric_cls = METRIC_REGISTRY.get(name)
        if not metric_cls:
            raise ValueError(f"Unknown metric: {name}")
        metrics.append(metric_cls())

    for event in parser.parse(args.logfile):
        for metric in metrics:
            metric.consume(event)

    formatter = JsonReportFormatter()
    print(formatter.format(metrics))



if __name__ == "__main__":
    main()
