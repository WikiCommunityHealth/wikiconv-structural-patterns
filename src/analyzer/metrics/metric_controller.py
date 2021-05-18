from typing import Any, Dict, List
from .. import utils
from ..database import Database, MetricDB, BufferMetricDB
from .metric import Record, Metric
from .metric_action_type import MetricActionType
from .metric_discussion_depth import MetricDiscussionDepth
from .metric_toxicity import MetricToxicity
from .metric_user_involved import MetricUserInvolved
from .metric_vandalism import MetricVandalism

mapper = {
    "action_type": MetricActionType,
    "discussion_depth": MetricDiscussionDepth,
    "toxicity": MetricToxicity,
    "user_involved": MetricUserInvolved,
    "vandalism": MetricVandalism,
    # chain: ,
}


class MetricController:
    def __init__(self, configs: Dict[str, Any]):
        configs_general = configs["general"]
        configs_database = configs["database"]
        configs_metric = configs["metrics"]

        assert configs_general
        assert configs_database
        assert configs_metric

        self.target_analysis = configs_general["target_field"]
        self.buffer_size = configs_general["buffer_size"]

        self.database = Database(
            dbname=configs_database["dbname"],
            table=configs_database["table"],
            user=configs_database["user"],
            password=configs_database["password"],
            host=configs_database.get("host", "localhost"),
            port=configs_database.get("port", 5432),
        )

        self.buffer = BufferMetricDB(self.buffer_size, self.database)

        self.metrics: List[Metric] = []
        for metric_name, is_required in configs_metric.items():
            if is_required:
                assert metric_name in mapper
                self.metrics.append(mapper[metric_name]())

    def calculate_metrics_for_block(self, records: List[Record], block_id: str):
        for metric_type in self.metrics:
            new_metrics = metric_type.calculate_metric_for_block(records, block_id)
            self.buffer.extend(new_metrics)

    def flush(self):
        self.buffer.flush()

    # def add_record(self, record: Dict[str, Any]):
    #     """
    #     Add new information to metrics for the current page
    #     """
    #     username: str = utils.get_username(record)
    #     current_year_month: str = utils.get_year_month_from_timestamp(
    #         record["timestamp"]
    #     )

    #     self.m_action_type.add_info(record["type"], current_year_month)
    #     self.m_user_involved.add_info(username, current_year_month)

    #     if "indentation" in record:
    #         self.m_discussion_depth.add_info(
    #             int(record["indentation"]), current_year_month
    #         )

    #     if "score" in record:
    #         self.m_toxicity.add_info(record["score"], current_year_month)

    #     if "comment" in record:
    #         self.m_vandalism.add_info(record["comment"], current_year_month)