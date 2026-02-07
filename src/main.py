import argparse

from src.parser.log_parser import LogParser
from src.metrics.request_count import RequestCountMetric
from src.metrics.error_rate import ErrorRateMetric
from src.metrics.latency import LatencyMetric
from src.report.formatter import JsonReportFormatter


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
    return parser


def main():
    arg_parser = build_arg_parser()
    args = arg_parser.parse_args()

    parser = LogParser()

    metrics = [
        RequestCountMetric(),
        ErrorRateMetric(),
        LatencyMetric(),
    ]

    for event in parser.parse(args.logfile):
        for metric in metrics:
            metric.consume(event)

    formatter = JsonReportFormatter()
    output = formatter.format(metrics)

    print(output)


if __name__ == "__main__":
    main()
