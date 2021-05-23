from typing import Dict, List
from .metric import Metric, Record
from ..database import MetricDB


class MetricHIndex(Metric):
    """
    h-index: maximum number h s.t. there are >= h messages with depth >= h
    """

    def _output_metrics(self, depth_by_month: dict, block_id: str) -> List[MetricDB]:
        hindexes = {}
        current_depths = {}
        max_hindex = -1

        for year_month, indentations in depth_by_month.items():
            for indentation, value in indentations.items():
                if indentation not in current_depths:
                    current_depths[indentation] = value
                else:
                    current_depths[indentation] += value

            hindex = 0
            for indentation, value in sorted(current_depths.items()):
                if value >= indentation:
                    hindex = indentation
                    max_hindex = max(hindex, max_hindex)
                else:
                    break

            hindexes[year_month] = hindex

        output: List[MetricDB] = []

        for year_month, value in sorted(hindexes.items()):
            output.append(
                MetricDB(
                    block_id=block_id,
                    metric_name="hindex",
                    year_month=year_month,
                    abs_actual_value=value,
                    rel_actual_value=value / max_hindex,
                    abs_cumulative_value=-1,
                    rel_cumulative_value=-1,
                )
            )

        if output:
            output[-1].rel_cumulative_value = 1

        return output

    def calculate_metric_for_block(
        self, records: List[Record], block_id: str
    ) -> List[MetricDB]:
        output = []
        depth_by_month = {}

        for record in records:
            if "indentation" in record:
                indentation = record["indentation"]
                year_month = record["year_month"]

                value = 1
                if record["type"] == "DELETION":
                    value = -1

                if year_month not in depth_by_month:
                    depth_by_month[year_month] = {}
                    depth_by_month[year_month][indentation] = value
                else:
                    if indentation not in depth_by_month[year_month]:
                        depth_by_month[year_month][indentation] = value

        if len(records):
            output = self._output_metrics(depth_by_month, block_id)

        return output
