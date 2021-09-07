from typing import List
from .data import MetricOutput, ChainOutput
from .database import Database


class BufferMetricOutput:
    def __init__(self, max_size: int, database: Database) -> None:
        self.buffer: List[MetricOutput] = []
        self.max_size = max_size
        self.database = database

    def __len__(self):
        return len(self.buffer)

    def clean(self):
        self.buffer.clear()

    def extend(self, metrics: List[MetricOutput]):
        self.buffer.extend(metrics)

        if len(self.buffer) > self.max_size:
            self.flush()

    def flush(self):
        self.database.send_metric_data(self.buffer)
        self.clean()


class BufferChainOutput:
    def __init__(self, max_size: int, database: Database) -> None:
        self.buffer: List[ChainOutput] = []
        self.max_size = max_size
        self.database = database

    def __len__(self):
        return len(self.buffer)

    def clean(self):
        self.buffer.clear()

    def extend(self, chains: List[ChainOutput]):
        self.buffer.extend(chains)

        if len(self.buffer) > self.max_size:
            self.flush()

    def flush(self):
        self.database.send_chain_data(self.buffer)
        self.clean()
