# log-metrics-engine
Build a configurable log analysis system that parses application logs and generates metrics
# Log Metrics Engine

A streaming log analyzer written in Python that parses application logs and
generates useful metrics such as request count, error rate, and latency
percentiles.

## Goals
- Process large log files efficiently using streaming
- Generate configurable metrics
- Keep the system extensible and testable
- Follow clean architecture principles

## Example Metrics
- Total request count
- Error rate (5xx)
- Latency percentiles (p50, p95, max)

## Tech Stack
- Python 3
- Standard library only (initially)

## Project Structure

## Configuration

Metrics can be enabled or disabled using a YAML configuration file.

Example `metrics.yaml`:

```yaml
metrics:
  - request_count
  - error_rate

## Usage

Analyze a log file and generate metrics with config:

```bash
python -m src.main sample_logs/access.log --config config/metrics.yaml

## Sample Output

```json
{
  "request_count": 4,
  "error_count": 1,
  "error_rate_percent": 25.0,
  "latency_p50_ms": 116.5,
  "latency_p95_ms": 342,
  "latency_max_ms": 342
}
