from typing import Dict, List
from .metric import Metric, Record
from ..database import MetricDB


class MetricToxicity(Metric):
    """
    docstring
    """

    def _output_metrics_for_score(
        self, score_by_month: dict, score_name: str, count_score: int, block_id: str
    ) -> List[MetricDB]:
        output: List[MetricDB] = []

        cumulative_toxicity = 0
        for year_month, value in score_by_month.items():
            cumulative_toxicity += value
            output.append(
                MetricDB(
                    block_id=block_id,
                    metric_name=score_name,
                    year_month=year_month,
                    abs_actual_value=value,
                    rel_actual_value=value / count_score,
                    abs_cumulative_value=cumulative_toxicity,
                    rel_cumulative_value=cumulative_toxicity / count_score,
                )
            )

        return output

    def calculate_metric_for_block(
        self, records: List[Record], block_id: str
    ) -> List[MetricDB]:
        output = []
        toxicity_by_month = {}
        severe_toxicity_by_month = {}

        count_toxicity = 0
        count_severe_toxicity = 0

        for record in records:
            if "type" in record:
                if record["type"] == "DELETION":
                    continue
                # TODO: create new metrics to count number of toxic actions removed
            else:
                continue

            if "score" in record:
                year_month = record["year_month"]
                score = record["score"]

                if "toxicity" in score and score["toxicity"] >= 0.64:
                    toxicity_by_month[year_month] = (
                        toxicity_by_month.get(year_month, 0) + 1
                    )
                    count_toxicity += 1

                if "severeToxicity" in score and score["severeToxicity"] >= 0.92:
                    severe_toxicity_by_month[year_month] = (
                        severe_toxicity_by_month.get(year_month, 0) + 1
                    )
                    count_severe_toxicity += 1

        if toxicity_by_month:
            output.extend(
                self._output_metrics_for_score(
                    toxicity_by_month,
                    "toxicity",
                    count_toxicity,
                    block_id,
                )
            )

        if severe_toxicity_by_month:
            output.extend(
                self._output_metrics_for_score(
                    severe_toxicity_by_month,
                    "severeToxicity",
                    count_severe_toxicity,
                    block_id,
                )
            )

        return output
