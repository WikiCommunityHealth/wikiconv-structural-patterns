from typing import Dict, List
from .metric import Metric, Record
from ..output import MetricOutput


class MetricVandalism(Metric):
    """
    it - vandalismo
    es - vandalismo
    ca - vandalisme
    en - vandalism
    """

    def _output_metrics(
        self, vandalism_by_month: dict, count_vandal: int, block_id: str
    ) -> List[MetricOutput]:
        output: List[MetricOutput] = []

        cumulative_vandalism = 0
        for year_month, value in vandalism_by_month.items():
            cumulative_vandalism += value
            output.append(
                MetricOutput(
                    block_id=block_id,
                    metric_name="vandalism",
                    year_month=year_month,
                    abs_actual_value=value,
                    rel_actual_value=value / count_vandal,
                    abs_cumulative_value=cumulative_vandalism,
                    rel_cumulative_value=cumulative_vandalism / count_vandal,
                )
            )

        return output

    def calculate_metric_for_block(
        self, records: List[Record], block_id: str
    ) -> List[MetricOutput]:
        output = []
        vandalism_by_month = {}
        count_vandal = 0

        for record in records:
            comment = record.get("comment", "")
            year_month = record["year_month"]

            if "vandalism" in comment.lower():
                vandalism_by_month[year_month] = (
                    vandalism_by_month.get(year_month, 0) + 1
                )
                count_vandal += 1

        if vandalism_by_month:
            output = self._output_metrics(
                vandalism_by_month, count_vandal, block_id
            )

        return output