from src.parser.log_parser import LogParser
from src.metrics.request_count import RequestCountMetric
from src.metrics.error_rate import ErrorRateMetric
from src.metrics.latency import LatencyMetric
from src.report.formatter import JsonReportFormatter


def main():
    parser = LogParser()

    metrics = [
        RequestCountMetric(),
        ErrorRateMetric(),
        LatencyMetric(),
    ]

    for event in parser.parse("sample_logs/access.log"):
        for metric in metrics:
            metric.consume(event)

    formatter = JsonReportFormatter()
    report = formatter.format(metrics)

    print(report)


if __name__ == "__main__":
    main()
