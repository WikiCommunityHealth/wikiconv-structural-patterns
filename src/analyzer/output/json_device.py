import json

from typing import List
from .data import MetricOutput, ChainOutput
from .device import Device

class JsonDevice(Device):
    def __init__(self, filename_metric: str, filename_chains: str, reset: bool) -> None:
        mode = 'w' if reset else 'a' 
        self.file_metrics = open(filename_metric, mode)
        self.file_chains = open(filename_chains, mode)
    
    def send_metric_data(self, data: List[MetricOutput]):
        objs = [f"{json.dumps(obj.unpack(), default=str)}\n" for obj in data]
        self.file_metrics.writelines(objs)

    def send_chain_data(self, data: List[ChainOutput]):
        objs = [f"{json.dumps(obj.unpack(), default=str)}\n" for obj in data]
        self.file_chains.writelines(objs)

    def close(self):
        self.file_metrics.close()
        self.file_chains.close()
