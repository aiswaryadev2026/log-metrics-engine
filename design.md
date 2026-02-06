# Log Metrics Engine - Design Document

## Overview
The Log Metrics Engine is a streaming log analyzer that processes application logs and generates configurable metrics. It follows a clean architecture with separation of concerns, making it extensible and testable.

## Architecture

### High-Level Architecture Diagram
```
┌─────────────────┐
│   Log File      │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  LogParser          │
│  (Streaming)        │
└────────┬────────────┘
         │
         │ Iterator[LogEvent]
         ▼
┌──────────────────────────────────────┐
│         Main Event Loop              │
│  Distributes events to metrics       │
└──────────────────────────────────────┘
         │
    ┌────┼────┐
    │    │    │
    ▼    ▼    ▼
┌────────────────────────────────────────┐
│  Metrics (Consume & Calculate)         │
├────────────────────────────────────────┤
│ • RequestCountMetric                   │
│ • ErrorRateMetric                      │
│ • LatencyMetric                        │
└────────────────────────────────────────┘
         │
         ▼
┌──────────────────────┐
│  Results (Aggregate) │
│  & Print             │
└──────────────────────┘
```

## Core Components

### 1. **Data Model** (`src/model/event.py`)
**LogEvent** - Immutable domain object representing a single log entry
- `timestamp: datetime` - When the request occurred (ISO-8601)
- `method: str` - HTTP method (GET, POST, etc.)
- `path: str` - URL path
- `status: int` - HTTP response status code
- `latency_ms: int` - Response time in milliseconds

### 2. **Parser** (`src/parser/log_parser.py`)
**LogParser** - Streaming parser that converts raw log lines into LogEvent objects
- Accepts file path, returns `Iterator[LogEvent]`
- Parses lines in format: `<timestamp> <method> <path> <status> <latency_ms>`
- Example format: `2024-09-10T10:15:30Z GET /api/orders 200 123`
- Handles ISO-8601 Zulu time format
- Detailed error messages with line numbers for parsing failures

### 3. **Base Metric** (`src/metrics/base.py`)
**Metric** - Abstract base class defining the metric interface
```python
class Metric(ABC):
    @abstractmethod
    def consume(self, event: LogEvent) -> None:
        """Process an event and update internal state."""
        pass

    @abstractmethod
    def result(self) -> dict:
        """Return computed metric as a dictionary."""
        pass
```

### 4. **Metric Implementations**

#### **RequestCountMetric** (`src/metrics/request_count.py`)
Tracks total number of requests processed
- Increments counter for each event
- **Output**: `{"request_count": int}`

#### **ErrorRateMetric** (`src/metrics/error_rate.py`)
Calculates the percentage of server errors (5xx status codes)
- Tracks total requests and 5xx error count
- Calculates percentage with 2 decimal precision
- **Output**: 
  ```python
  {
    "error_count": int,
    "error_rate_percent": float
  }
  ```

#### **LatencyMetric** (`src/metrics/latency.py`)
Computes latency percentiles and maximum
- Stores all latency values
- Calculates: p50 (median), p95, and max
- **Output**: 
  ```python
  {
    "latency_p50_ms": float,
    "latency_p95_ms": float,
    "latency_max_ms": int
  }
  ```

## Workflow / Data Flow

### Step 1: Initialization
Main entry point instantiates:
1. `LogParser()` - for parsing log files
2. List of metrics objects:
   - `RequestCountMetric()`
   - `ErrorRateMetric()`
   - `LatencyMetric()`

### Step 2: Streaming & Processing
```python
for event in parser.parse("sample_logs/access.log"):
    for metric in metrics:
        metric.consume(event)
```

**Process:**
1. LogParser opens and reads log file line-by-line
2. For each valid line, creates a LogEvent object
3. Yields event to main loop (streaming, not loading entire file)
4. Each metric receives the event via `consume()`
5. Metric updates its internal state
6. Loop continues to next event

### Step 3: Results Aggregation
```python
for metric in metrics:
    print(metric.result())
```

1. After all events are processed, call `result()` on each metric
2. Each metric returns a dictionary with computed values
3. Results are printed to stdout

## Key Design Patterns

### Streaming/Iterator Pattern
- Parser uses generators (`yield`) to process logs memory-efficiently
- Suitable for large log files that don't fit in memory
- Events are processed one at a time

### Abstract Base Class Pattern
- `Metric` ABC enforces interface contract
- Enables easy addition of new metric types
- All metrics implement `consume()` and `result()`

### Immutable Domain Objects
- `LogEvent` is a frozen dataclass
- Thread-safe by design
- Prevents accidental state mutations

## Extensibility Points

### Adding New Metrics
1. Create a new class inheriting from `Metric`
2. Implement `consume(event)` - update internal state
3. Implement `result()` - return computed values
4. Add instance to metrics list in `main()`

Example:
```python
class MyCustomMetric(Metric):
    def __init__(self):
        self._state = {}
    
    def consume(self, event: LogEvent) -> None:
        # Process event
        pass
    
    def result(self) -> dict:
        # Return computed metric
        return {}
```

### Enhancing LogEvent
- Add new fields to `LogEvent` dataclass
- Update parser to extract new fields from logs
- Leverage new fields in metrics

### Changing Log Format
- Update `LogParser._parse_line()` regex/parsing logic
- Maintain same `LogEvent` interface
- All metrics continue working without changes

## Testing Strategy

The project includes comprehensive unit tests:
- **test_parser.py** - LogParser functionality
- **test_event.py** - LogEvent creation and properties
- **test_request_count_metric.py** - RequestCountMetric calculations
- **test_error_rate_metric.py** - ErrorRateMetric calculations
- **test_latency_metric.py** - LatencyMetric calculations

Tests use temporary files to avoid dependencies on sample data.

## Dependencies

- **Python 3.x** - Standard library only
- **statistics module** - For percentile calculations
- **dataclasses** - For domain objects
- **typing** - For type hints

## Running the Application

```bash
python -m src.main
```

Input: `sample_logs/access.log`
Output: Metrics summary printed to stdout

Example output:
```
Metrics summary:
{'request_count': 1000}
{'error_count': 25, 'error_rate_percent': 2.5}
{'latency_p50_ms': 125.0, 'latency_p95_ms': 450, 'latency_max_ms': 2500}
```

## Future Enhancements

1. **Configuration** - YAML/JSON config files to specify metrics and output formats
2. **Output Formats** - JSON, CSV, Prometheus metrics format
3. **Time Windows** - Calculate metrics per minute/hour (sliding windows)
4. **Filtering** - Pre-process events (e.g., filter by path, status, etc.)
5. **Aggregation** - Group metrics by path, method, status code
6. **Performance** - Parallel metric processing for multi-core systems
