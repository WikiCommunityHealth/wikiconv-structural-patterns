from typing import Dict, Set, List
from .metric import Metric, Record
from ..output import MetricOutput


class MetricUserInvolved(Metric):
    """
    docstring
    """

    def _output_metrics(
        self, new_users_by_month: dict, num_users: int, block_id: str
    ) -> List[MetricOutput]:
        output: List[MetricOutput] = []

        cumulative_num_users = 0
        for year_month, new_users in new_users_by_month.items():
            cumulative_num_users += new_users

            output.append(
                MetricOutput(
                    block_id=block_id,
                    metric_name="user_involved",
                    year_month=year_month,
                    abs_actual_value=new_users,
                    rel_actual_value=new_users / num_users,
                    abs_cumulative_value=cumulative_num_users,
                    rel_cumulative_value=cumulative_num_users / num_users,
                )
            )

        return output

    def calculate_metric_for_block(
        self, records: List[Record], block_id: str
    ) -> List[MetricOutput]:
        output = []
        users = set()
        new_users_by_month = {}
        
        for record in records:
            username = record["username"]
            year_month = record["year_month"]

            if username not in users:
                users.add(username)
                new_users_by_month[year_month] = (
                    new_users_by_month.get(year_month, 0) + 1
                )

        if new_users_by_month:
            output = self._output_metrics(
                new_users_by_month, len(users), block_id
            )

        return output


    # def __init__(self):
    #     self.users: Set[str] = set()
    #     self.new_users_by_month: Dict[str, int] = {}

    # def reset(self):
    #     self.users.clear()
    #     self.new_users_by_month.clear()

    # def calculate(self, page_id: int) -> List[MetricDB]:
    #     total_users = len(self.users)
    #     output: List[MetricDB] = []

    #     cumulative_num_users = 0
    #     for year_month, new_users in self.new_users_by_month.items():
    #         cumulative_num_users += new_users

    #         output.append(
    #             MetricDB(
    #                 block_id=page_id,
    #                 metric_name="user_involved",
    #                 year_month=year_month,
    #                 abs_actual_value=new_users,
    #                 rel_actual_value=new_users / total_users,
    #                 abs_cumulative_value=cumulative_num_users,
    #                 rel_cumulative_value=cumulative_num_users / total_users,
    #             )
    #         )

    #     return output

    # def add_info(self, username: str, current_year_month: str):
    #     if username not in self.users:
    #         self.users.add(username)
    #         self.new_users_by_month[current_year_month] = (
    #             self.new_users_by_month.get(current_year_month, 0) + 1
    #         )
