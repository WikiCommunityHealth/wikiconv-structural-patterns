from typing import Dict, List
from .metric import Metric, Record
from ..database import MetricDB


class MetricActionType(Metric):
    """
    Number of different types of actions
    """

    def _output_metrics(
        self, actions_by_month: dict, num_records: int, block_id: str
    ) -> List[MetricDB]:
        output: List[MetricDB] = []

        cumulative_values = {
            "CREATION": 0,
            "ADDITION": 0,
            "MODIFICATION": 0,
            "DELETION": 0,
            "RESTORATION": 0,
            "TOTAL": 0,
        }

        for year_month, actions in actions_by_month.items():
            num_actions_current_month = 0
            for action, value in actions.items():
                cumulative_values[action] += value
                num_actions_current_month += value
                output.append(
                    MetricDB(
                        block_id=block_id,
                        metric_name="num_action_" + action.lower(),
                        year_month=year_month,
                        abs_actual_value=value,
                        rel_actual_value=value / num_records,
                        abs_cumulative_value=cumulative_values[action],
                        rel_cumulative_value=cumulative_values[action] / num_records,
                    )
                )

            cumulative_values["TOTAL"] += num_actions_current_month
            output.append(
                MetricDB(
                    block_id=block_id,
                    metric_name="total_action",
                    year_month=year_month,
                    abs_actual_value=num_actions_current_month,
                    rel_actual_value=num_actions_current_month / num_records,
                    abs_cumulative_value=cumulative_values["TOTAL"],
                    rel_cumulative_value=cumulative_values["TOTAL"] / num_records,
                )
            )

        return output

    def calculate_metric_for_block(
        self, records: List[Record], block_id: str
    ) -> List[MetricDB]:
        output = []
        actions_by_month = {}

        for record in records:
            action_type = record["type"]
            year_month = record["year_month"]
            if year_month not in actions_by_month:
                actions_by_month[year_month] = {
                    "CREATION": 0,
                    "ADDITION": 0,
                    "MODIFICATION": 0,
                    "DELETION": 0,
                    "RESTORATION": 0,
                    "TOTAL": 0,
                }

            actions_by_month[year_month][action_type] += 1
            actions_by_month[year_month]["TOTAL"] += 1

        if len(records):
            output = self._output_metrics(actions_by_month, len(records), block_id)

        return output
