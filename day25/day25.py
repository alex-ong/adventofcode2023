"""day25 solution"""
from dataclasses import dataclass

import matplotlib.pyplot as plt
import networkx as nx

INPUT_SMALL = "day25/input-small.txt"
INPUT = "day25/input.txt"
SHOW_GRAPH = False


@dataclass
class Connection:
    src: str
    dests: list[str]

    def node_names(self) -> list[str]:
        return [self.src] + self.dests


def parse_connection(line: str) -> Connection:
    src, dests = line.split(":")
    return Connection(src, dests.split())


def get_data(path: str) -> list[Connection]:
    connections: list[Connection] = []
    with open(path, "r", encoding="utf8") as file:
        for line in file:
            connections.append(parse_connection(line))

    return connections


def show_graph(graph: nx.Graph) -> None:  # pragma: no cover
    """Draws a graph that you can see"""
    nx.draw(graph, with_labels=True)
    plt.draw()
    plt.show()


def solve_nodes(connections: list[Connection]) -> int:
    """Graphs the modules"""
    G = nx.Graph()

    nodes: set[str] = set()
    for connection in connections:
        to_add = connection.node_names()
        for node_name in to_add:
            if node_name not in nodes:
                nodes.add(node_name)
                G.add_node(node_name)
            if node_name != connection.src:
                G.add_edge(connection.src, node_name)
    if SHOW_GRAPH:  # pragma: no cover
        show_graph(G)
    cut_value, partition = nx.stoer_wagner(G)
    print(f"num_cuts: {cut_value}")
    return len(partition[0]) * len(partition[1])


def main() -> None:
    conns = get_data(INPUT)
    result = solve_nodes(conns)
    print(result)


if __name__ == "__main__":
    main()
