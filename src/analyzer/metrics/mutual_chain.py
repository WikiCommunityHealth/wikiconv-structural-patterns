from typing import Dict
from .metric import Metric

import networkx as nx


class MutualChain(Metric):
    """
    docstring
    """

    # def __init__(self):
    #     self.visited: Dict[str, bool] = {}
    #     self.G = nx.DiGraph()
    #     self.chains = {}
    #     self.num_chains = 0

    # def reset(self):
    #     self.visited.clear()
    #     self.G.clear()
    #     self.chains.clear()
    #     self.num_chains = 0

    # def calculate(self):
    #     self.visited = dict(zip(self.G.nodes, [False] * len(self.G.nodes)))
    #     for node in self.G.nodes:
    #         if not self.visited[node]:
    #             self.dfs_rec(node, None, False, None, 2)

    #     return self.chains

    # def add_info(self, record, username):
    #     self.G.add_node(
    #         record["id"],
    #         user=username,
    #         action=record["type"],
    #         timestamp=record["timestamp"],
    #     )

    #     if "replytoId" in record and record["replytoId"] != None:
    #         self.G.add_edge(record["replytoId"], record["id"])

    # def dfs_rec(self, node, last, is_chain, timestamp_begin_chain, chain_length):
    #     self.visited[node] = True
    #     has_mutual_response = False

    #     for adj in self.G[node]:
    #         if not self.visited[adj]:
    #             try:
    #                 if (
    #                     last != None
    #                     and self.G.nodes[last] != {}
    #                     and self.G.nodes[last]["user"] == self.G.nodes[adj]["user"]
    #                     and self.G.nodes[last]["user"] != self.G.nodes[node]["user"]
    #                 ):
    #                     has_mutual_response = True
    #                     if timestamp_begin_chain == None:
    #                         timestamp_begin_chain = self.G.nodes[last]["timestamp"]
    #                     self.dfs_rec(
    #                         adj, node, True, timestamp_begin_chain, chain_length + 1
    #                     )
    #                 else:
    #                     self.dfs_rec(adj, node, False, None, 2)
    #             except Exception:
    #                 print(last, self.G.nodes[last])
    #                 print(adj, self.G.nodes[adj])

    #     if is_chain and not has_mutual_response:
    #         timestamp_end_chain = self.G.nodes[node]["timestamp"]
    #         current_month_year = (
    #             f"{timestamp_end_chain.month}/{timestamp_end_chain.year}"
    #         )

    #         self.num_chains += 1

    #         if current_month_year not in self.chains:
    #             self.chains[current_month_year] = []

    #         # use length to get who started the chain
    #         if chain_length % 2 == 0:
    #             # print(f"{self.G.nodes[last]['user']}<->{self.G.nodes[node]['user']}: started at {timestamp_begin_chain} with length {chain_length}")
    #             self.chains[current_month_year].append(
    #                 {
    #                     "first": self.G.nodes[last]["user"],
    #                     "second": self.G.nodes[node]["user"],
    #                     "timestamp_begin": timestamp_begin_chain,
    #                     "timestamp_end": timestamp_end_chain,
    #                     "duration_sec": (
    #                         timestamp_end_chain - timestamp_begin_chain
    #                     ).seconds,
    #                     "length": chain_length,
    #                 }
    #             )
    #         else:
    #             # print(f"{self.G.nodes[node]['user']}<->{self.G.nodes[last]['user']}: started at {timestamp_begin_chain} with length {chain_length}")

    #             self.chains[current_month_year].append(
    #                 {
    #                     "first": self.G.nodes[node]["user"],
    #                     "second": self.G.nodes[last]["user"],
    #                     "timestamp_begin": timestamp_begin_chain,
    #                     "timestamp_end": timestamp_end_chain,
    #                     "duration_sec": (
    #                         timestamp_end_chain - timestamp_begin_chain
    #                     ).seconds,
    #                     "length": chain_length,
    #                 }
    #             )
