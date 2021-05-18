from typing import Dict, List
from .metric import Metric, Record
from ..database import MetricDB


class MetricDiscussionDepth(Metric):
    """
    docstring
    """

    def _output_metrics(
        self, depth_by_month: dict, max_depth: int, block_id: str
    ) -> List[MetricDB]:
        output: List[MetricDB] = []
        current_max_depth = -1

        for year_month, value in depth_by_month.items():
            current_max_depth = max(current_max_depth, value)
            output.append(
                MetricDB(
                    block_id=block_id,
                    metric_name="max_depth",
                    year_month=year_month,
                    abs_actual_value=value,
                    rel_actual_value=value / max_depth,
                    abs_cumulative_value=current_max_depth,
                    rel_cumulative_value=current_max_depth / max_depth,
                )
            )
        return output

    def calculate_metric_for_block(
        self, records: List[Record], block_id: str
    ) -> List[MetricDB]:
        output = []
        depth_by_month = {}
        max_depth = -1

        for record in records:
            if "indentation" in record:
                indentation = record["indentation"]
                year_month = record["year_month"]
                max_depth = max(max_depth, indentation)

                if year_month not in depth_by_month:
                    depth_by_month[year_month] = indentation
                else:
                    depth_by_month[year_month] = max(
                        indentation, depth_by_month[year_month]
                    )

        if len(records):
            # output = self.output_metrics(depth_by_month, max_depth, block_id)
            output = self._output_metrics(
                depth_by_month, max_depth, records[0]["pageTitle"]
            )

        return output
