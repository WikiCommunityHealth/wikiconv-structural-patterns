from typing import Any, Dict, List, Tuple
from .metric import Metric, Record
from ..output import ChainOutput, MetricOutput

import networkx as nx


class MetricChain(Metric):
    """
    Mutual chain of responses detection
    """

    def dfs_rec(self, node, last, is_chain, timestamp_begin_chain, chain_length):
        self.visited[node] = True
        has_mutual_response = False

        for adj in self.G[node]:
            if not self.visited[adj]:
                try:
                    if (
                        last != None
                        and self.G.nodes[last] != {}
                        and self.G.nodes[last]["user"] == self.G.nodes[adj]["user"]
                        and self.G.nodes[last]["user"] != self.G.nodes[node]["user"]
                    ):
                        has_mutual_response = True
                        if timestamp_begin_chain == None:
                            timestamp_begin_chain = self.G.nodes[last]["timestamp"]
                        self.dfs_rec(
                            adj, node, True, timestamp_begin_chain, chain_length + 1
                        )
                    else:
                        self.dfs_rec(adj, node, False, None, 2)
                except Exception:
                    print(last, self.G.nodes[last])
                    print(adj, self.G.nodes[adj])

        if is_chain and not has_mutual_response:
            timestamp_end_chain = self.G.nodes[node]["timestamp"]
            year_month = self.G.nodes[node]["year_month"]

            self.num_chains += 1
            self.num_chain_messages += chain_length

            if year_month not in self.chains:
                self.chains[year_month] = []

            # use length to get who started the chain
            if chain_length % 2 == 0:
                # print(f"{self.G.nodes[last]['user']}<->{self.G.nodes[node]['user']}: started at {timestamp_begin_chain} with length {chain_length}")
                self.chains[year_month].append(
                    {
                        "first": self.G.nodes[last]["user"],
                        "second": self.G.nodes[node]["user"],
                        "year_month": year_month,
                        "timestamp_begin": timestamp_begin_chain,
                        "timestamp_end": timestamp_end_chain,
                        "duration_sec": (
                            timestamp_end_chain - timestamp_begin_chain
                        ).seconds,
                        "length": chain_length,
                    }
                )
            else:
                # print(f"{self.G.nodes[node]['user']}<->{self.G.nodes[last]['user']}: started at {timestamp_begin_chain} with length {chain_length}")

                self.chains[year_month].append(
                    {
                        "first": self.G.nodes[node]["user"],
                        "second": self.G.nodes[last]["user"],
                        "year_month": year_month,
                        "timestamp_begin": timestamp_begin_chain,
                        "timestamp_end": timestamp_end_chain,
                        "duration_sec": (
                            timestamp_end_chain - timestamp_begin_chain
                        ).seconds,
                        "length": chain_length,
                    }
                )

    def _output_metrics(self, depth_by_month: dict, block_id: str) -> List[MetricOutput]:
        output: List[MetricOutput] = []

        self.visited = dict(zip(self.G.nodes, [False] * len(self.G.nodes)))
        for node in self.G.nodes:
            if not self.visited[node]:
                self.dfs_rec(node, None, False, None, 2)

        cumulative_messages = 0
        cumulative_chains = 0

        for year_month, chains in self.chains.items():
            curr_messages = 0
            curr_chains = 0

            for chain in chains:
                curr_messages += chain["length"]
                curr_chains += 1

            cumulative_messages += curr_messages
            cumulative_chains += curr_chains

            output.append(
                MetricOutput(
                    block_id=block_id,
                    metric_name="message_chains",
                    year_month=year_month,
                    abs_actual_value=curr_messages,
                    rel_actual_value=curr_messages / self.num_chain_messages,
                    abs_cumulative_value=cumulative_messages,
                    rel_cumulative_value=cumulative_messages / self.num_chain_messages,
                )
            )

            output.append(
                MetricOutput(
                    block_id=block_id,
                    metric_name="num_chains",
                    year_month=year_month,
                    abs_actual_value=curr_chains,
                    rel_actual_value=curr_chains / self.num_chains,
                    abs_cumulative_value=cumulative_chains,
                    rel_cumulative_value=cumulative_chains / self.num_chains,
                )
            )

        return output

    def calculate_metric_for_block(
        self, records: List[Record], block_id: str
    ) -> Tuple[List[MetricOutput], List[ChainOutput]]:
        output = []
        depth_by_month = {}

        self.G = nx.DiGraph()

        for record in records:
            self.G.add_node(
                record["id"],
                user=record["username"],
                action=record["type"],
                timestamp=record["timestamp"],
                year_month=record["year_month"],
            )

            if "replytoId" in record and record["replytoId"] != None:
                self.G.add_edge(record["replytoId"], record["id"])

        self.visited = dict(zip(self.G.nodes, [False] * len(self.G.nodes)))
        self.chains = {}
        self.num_chains = 0
        self.num_chain_messages = 0

        if len(records):
            output = self._output_metrics(depth_by_month, block_id)

        self.visited.clear()
        self.G.clear()
        # self.chains.clear()
        self.num_chains = 0
        self.num_chain_messages = 0

        chain_dbs: List[ChainOutput] = []

        for year_month, chains in self.chains.items():
            for chain in chains:
                chain_dbs.append(
                    ChainOutput(
                        chain["first"],
                        chain["second"],
                        chain["year_month"],
                        chain["timestamp_begin"],
                        chain["timestamp_end"],
                        chain["duration_sec"],
                        chain["length"],
                    )
                )

        return (output, chain_dbs)
