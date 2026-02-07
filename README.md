# log-metrics-engine

A streaming log analyzer written in Python that parses application logs and
generates configurable metrics such as request count, error rate, and latency
percentiles.

## Why Log Metrics Engine?

This project was built to demonstrate how to design a production-style
log processing system with:
- Streaming processing for large log files
- Fault-tolerant parsing
- Config-driven, pluggable metrics
- Clear separation between parsing, processing, and reporting

It is intentionally designed as a small but extensible system rather than
a one-off script.


## Features
- Stream large log files efficiently
- Configure which metrics to compute via YAML
- Extensible metric registry for easy addition of new metrics
- Small, well-tested codebase

## Fault Tolerance

The parser is designed to be fault tolerant:
- Malformed log lines do not stop processing
- Invalid lines are skipped and logged
- Parse failures can be tracked using the `parse_errors` metric

This ensures that a single bad log entry does not break the entire analysis.

## Prerequisites
- Python 3.8 or newer
- Git (optional)

## Quick install
Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the CLI against a log file. By default, if no `--config` is supplied the
tool enables `request_count`, `error_rate` and `latency` metrics.

```bash
python -m src.main sample_logs/access.log --config config/metrics.yaml

# or (use default metrics)
python -m src.main sample_logs/access.log
```

Options:
- `--config`: path to a YAML file that lists enabled metrics under the `metrics` key
- `--format`: output format (currently only `json`)

## Configuration

Example `config/metrics.yaml`:

```yaml
metrics:
  - request_count
  - error_rate
  - latency
```

Supported metric names are: `request_count`, `error_rate`, `latency`.
If an unknown metric name is present the CLI will raise `ValueError`.

## Sample output

When run, the program prints a JSON object summarizing computed metrics, for
example:

```json
{
  "request_count": 4,
  "error_count": 1,
  "error_rate_percent": 25.0,
  "latency_p50_ms": 116.5,
  "latency_p95_ms": 342,
  "latency_max_ms": 342
}
```

Field notes:
- `error_rate_percent`: percentage of error (5xx) responses
- latency fields are in milliseconds

## Running tests

Run the test suite with `pytest`:

```bash
pytest
```

## Project layout

See the `src/` package for implementation. Key modules:
- `src/parser/log_parser.py` - log line -> event parsing
- `src/metrics/*` - metric implementations and registry
- `src/report/formatter.py` - output formatting
- `src/config/loader.py` - YAML config loader

## Project Status

Current version: v1.0.0

This project is stable and suitable for learning, experimentation,
and small-scale log analysis. Future versions may introduce additional
output formats and integrations.

## Contributing

Contributions welcome — open an issue or submit a pull request. Add tests
for any new metric or parser behavior. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.
