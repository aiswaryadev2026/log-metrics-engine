from src.metrics.base import Metric


class ParseErrorMetric(Metric):
    def __init__(self):
        self._errors = 0

    def consume(self, event):
        # Only called for valid events
        pass

    def consume_error(self):
        self._errors += 1

    def result(self):
        return {"parse_errors": self._errors}
