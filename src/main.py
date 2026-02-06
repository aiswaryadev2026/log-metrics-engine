from src.parser.log_parser import LogParser
from src.metrics.request_count import RequestCountMetric
from src.metrics.error_rate import ErrorRateMetric
from src.metrics.latency import LatencyMetric


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

    print("Metrics summary:")
    for metric in metrics:
        print(metric.result())


if __name__ == "__main__":
    main()
