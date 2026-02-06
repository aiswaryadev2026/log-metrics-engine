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