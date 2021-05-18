from abc import ABC, abstractmethod
from typing import Any, List, Dict
from ..database import MetricDB

Record = Dict[str, Any]


class Metric(ABC):
    # @abstractmethod
    # def reset(self) -> None:
    #     ...

    # @abstractmethod
    # def calculate(self, page_id: int) -> List[MetricDB]:
    #     ...

    # @abstractmethod
    # def add_info(self, record: Record) -> None:
    #     ...

    @abstractmethod
    def calculate_metric_for_block(
        self, records: List[Record], block_id: str
    ) -> List[MetricDB]:
        ...
