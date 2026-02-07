# Log Metrics Engine - Design Document

## Overview
The Log Metrics Engine is a streaming log analyzer that processes application logs and generates configurable metrics. It follows a clean architecture with separation of concerns, making it extensible and testable.

## Architecture

### High-Level Architecture Diagram
```
┌─────────────────┐
│   Log File      │
"""Design document for Log Metrics Engine

This document describes the high-level design, data flow, and
extensibility points for the project. It also clarifies runtime behavior and
implementation trade-offs.
"""

# Log Metrics Engine — Design Document

## Overview
The Log Metrics Engine converts application log lines into domain events and
computes configurable metrics in a streaming fashion. The design prioritizes
low memory use, clear separation of concerns, and easy testing.

## Architecture

High-level flow:

```
Log File -> LogParser (generator) -> Main loop -> Metric instances -> Formatter
```

Components:
- `LogParser`: lazily parses lines and yields `LogEvent` objects
- `Main`: loads config, instantiates metrics from `METRIC_REGISTRY`, and
  executes the event loop
- `Metric` implementations: consume events and expose `result()`
- `Formatter`: serializes aggregated results (JSON by default)

Important note: metrics are instantiated from a registry (`src/metrics/registry.py`)
so the CLI can enable metrics by name from a YAML config without code edits.

## Core Components

### Data model (`src/model/event.py`)
`LogEvent` is a frozen dataclass representing a parsed log entry:

- `timestamp: datetime` — timezone-aware
- `method: str`
- `path: str`
- `status: int`
- `latency_ms: float`

Using `float` for `latency_ms` allows fractional values and consistent
calculations; keep `LogEvent` immutable for safety.

### Parser (`src/parser/log_parser.py`)
`LogParser.parse(path: str) -> Iterator[LogEvent]` parses a file line-by-line.

Recommended default format (configurable):
`<ISO8601-timestamp> <method> <path> <status> <latency_ms>`

Parser responsibilities:
- Parse lines into `LogEvent` objects
- Emit informative errors (including line numbers)
- Optionally run in a fault-tolerant mode (skip and log malformed lines)

### Metrics base & registry
`Metric` is an abstract base class with `consume(event: LogEvent)` and
`result() -> dict`.

`METRIC_REGISTRY: Dict[str, Type[Metric]]` maps metric names used in YAML to
their implementing classes. `main()` instantiates metrics by looking up names
from the loaded config.

### Example metrics

- `RequestCountMetric`: increments a counter per event. Output: `{"request_count": int}`
- `ErrorRateMetric`: tracks total and 5xx counts and returns `error_count` and
  `error_rate_percent` (float)
- `LatencyMetric`: computes p50/p95/max. Current implementation stores
  values in-memory; for very large inputs consider approximate, bounded-memory
  quantile algorithms (e.g., TDigest) and document this tradeoff.

## Workflow

1. Parse CLI args in `main()` and load YAML config (`src/config/loader.py`).
   If `--config` is omitted, default metrics are `request_count`, `error_rate`,
   and `latency`.
2. Instantiate metric classes from `METRIC_REGISTRY`.
3. Iterate `for event in LogParser.parse(path):` and call `metric.consume(event)`
   for each metric.
4. After processing, call `metric.result()` for each metric and pass the
   results to the `Formatter` for output.

Example conceptual loop:

```python
parser = LogParser()
metrics = [cls() for cls in metric_classes]
for event in parser.parse(logfile):
    for m in metrics:
        m.consume(event)
print(formatter.format(metrics))
```

## Testing strategy

- Unit tests cover parser behavior, `LogEvent` creation, and each metric.
- Parser tests include well-formed and malformed lines; fault-tolerant parsing
  is verified.
- Tests use temporary files where appropriate to avoid relying on sample data.

## Dependencies

- Python 3.8+
- `PyYAML` (runtime) — for config loading
- `pytest` (dev/test)

Update: README and older docs said "standard library only" — this project
depends on `PyYAML` at runtime (see `requirements.txt`).

## Running the application (CLI)

```bash
python -m src.main sample_logs/access.log --config config/metrics.yaml
```

Default metrics when `--config` is omitted: `request_count`, `error_rate`,
`latency`.

## Performance & scaling

- Storing all latency values is simple but O(n) memory — consider TDigest/GK
  for bounded memory quantiles.
- For high throughput, consider partitioning input and parallel metric
  processing; ensure metrics are thread-safe or use process-level sharding.

## Future work (prioritized)

1. Add bounded-memory/approximate quantiles for latency metrics.
2. Support additional output formats (CSV, Prometheus exposition).
3. Add time-windowed metrics and grouping by path/method.
4. Add CLI flags for fault-tolerant parsing and verbosity.
