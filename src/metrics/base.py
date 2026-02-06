from abc import ABC, abstractmethod
from src.model.event import LogEvent


class Metric(ABC):
    """
    Abstract base class for all metrics.
    """

    @abstractmethod
    def consume(self, event: LogEvent) -> None:
        """
        Consume a LogEvent and update internal state.
        """
        pass

    @abstractmethod
    def result(self) -> dict:
        """
        Return the computed metric as a dictionary.
        """
        pass
