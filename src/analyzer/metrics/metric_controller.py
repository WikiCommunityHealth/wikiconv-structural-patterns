from typing import Any, Dict, List
from .. import utils
from ..output import Database, MetricOutput, BufferMetricOutput, ChainOutput, BufferChainOutput
from ..output import JsonDevice
from .metric import Record, Metric
from .metric_action_type import MetricActionType
from .metric_discussion_depth import MetricDiscussionDepth
from .metric_toxicity import MetricToxicity
from .metric_user_involved import MetricUserInvolved
from .metric_vandalism import MetricVandalism
from .metric_h_index import MetricHIndex
from .mutual_chain import MetricChain
from analyzer import output

mapper = {
    "action_type": MetricActionType,
    "discussion_depth": MetricDiscussionDepth,
    "toxicity": MetricToxicity,
    "user_involved": MetricUserInvolved,
    "vandalism": MetricVandalism,
    "hindex": MetricHIndex,
    "chain": MetricChain,
}


class MetricController:
    def __init__(self, configs: Dict[str, Any]):
        output_device = configs["output_device"]

        configs_general = configs["general"]
        configs_metric = configs["metrics"]

        assert configs_general
        assert configs_metric

        self.target_analysis = configs_general["target_field"]
        self.buffer_size = configs_general["buffer_size"]
        self.filter_user_pages = configs_general["filter_user_pages"]

        if output_device == "database":
            configs_database = configs["database"]
            assert configs_database

            self.output = Database(
                dbname=configs_database["dbname"],
                table=configs_database["table"],
                user=configs_database["user"],
                password=configs_database["password"],
                host=configs_database.get("host", "localhost"),
                port=configs_database.get("port", 5432),
                reset=configs_database.get("reset", False)
            )
        elif output_device == "json":
            configs_json = configs["json"]
            assert configs_json

            self.output = JsonDevice(
                filename_metric=configs_json["filename"] + ".json",
                filename_chains=configs_json["filename"] + "_chains.json",
                reset=configs_json.get("reset", False)
            )
        else:
            assert False, "Unknown output device: " + output_device

        self.buffer_metrics = BufferMetricOutput(self.buffer_size, self.output)
        self.buffer_chains = BufferChainOutput(self.buffer_size, self.output)

        self.metrics: List[Metric] = []
        for metric_name, is_required in configs_metric.items():
            if is_required:
                assert metric_name in mapper
                self.metrics.append(mapper[metric_name]())

    def calculate_metrics_for_block(self, records: List[Record], block_id: str):
        for metric_type in self.metrics:
            new_metrics = []

            if isinstance(metric_type, MetricChain):
                new_metrics, chains = metric_type.calculate_metric_for_block(records, block_id)
                self.buffer_metrics.extend(new_metrics)
                self.buffer_chains.extend(chains)
            else:
                new_metrics = metric_type.calculate_metric_for_block(records, block_id)
                self.buffer_metrics.extend(new_metrics)
            
    def flush(self):
        self.buffer_metrics.flush()
        self.buffer_chains.flush()

    def close(self):
        self.output.close()
