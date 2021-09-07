from abc import ABC, abstractmethod
from typing import Any, List, Dict
from .data import MetricOutput, ChainOutput


class Device(ABC):
    @abstractmethod
    def send_metric_data(self, data: List[MetricOutput]):
        ...

    @abstractmethod
    def send_chain_data(self, data: List[ChainOutput]):
        ...

    @abstractmethod
    def close(self):
        ...
