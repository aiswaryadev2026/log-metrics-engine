# Contributing

Thanks for your interest in contributing to log-metrics-engine! We welcome
bug reports, feature requests, and pull requests. Please follow the guidelines
below to help us review and merge your changes quickly.

## How to contribute

- File an issue first for non-trivial changes so we can discuss the design.
- Fork the repository and create topic branches for your work (use descriptive
  branch names: `fix/parser-issue`, `feat/percentile-metric`).
- Keep changes small and focused; open multiple PRs if necessary.

## Development setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run tests locally:

```bash
pytest
```

## Coding guidelines

- Follow the existing project style: small functions, clear names, and type
  hints where appropriate.
- Add tests for new behavior or bug fixes. Tests live in the `tests/` folder
  and use `pytest`.
- Keep public APIs stable. If you need to change an API, explain the reason in
  the PR description and update tests and documentation.

## Adding a new metric

1. Implement the metric class under `src/metrics/` and ensure it adheres to
   the project's metric interface (see existing metrics for examples).
2. Register the metric in `src/metrics/registry.py` so it can be referenced by
   name from configuration files.
3. Add unit tests covering core behavior.

## Pull request checklist

- [ ] My changes include tests where applicable
- [ ] I ran the test suite (`pytest`) and all tests pass
- [ ] I updated documentation where necessary (README, examples)

## Issue reports

When filing issues, please include:
- A short descriptive title
- Steps to reproduce or a small sample log input
- Expected vs actual behavior
- Environment details (Python version)

## Code of conduct

Be respectful and collaborative. Open an issue if you need help or want to
discuss a proposed change.
