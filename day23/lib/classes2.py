"""part 2 solution"""
import time
from dataclasses import dataclass, field
from queue import Queue

import colorama

from day23.lib.classes import BasePath, Maze, Path, Position, Solver


@dataclass(eq=True)
class Node:
    name: int = field(compare=True)
    position: Position = field(compare=False)
    edges: list["Edge"] = field(default_factory=list, repr=False, compare=False)

    def __str__(self) -> str:
        return f"{self.name}: ({self.position}) {[str(edge) for edge in self.edges]}"


@dataclass
class Edge:
    node1: int
    node2: int
    path: Path = field(repr=False)

    def flip(self) -> "Edge":
        return Edge(self.node2, self.node1, self.path.flip())

    def __str__(self) -> str:
        return f"{self.node1}->{self.node2}, {len(self.path)}"

    def __len__(self) -> int:
        return len(self.path)


# Same thing as path but with nodes kappa
class NodePath(BasePath):
    path: list[int]
    node_ids: set[int]
    path_length: int

    def __init__(self) -> None:
        self.path = []
        self.node_ids = set()
        self.path_length = 0

    def can_add(self, node_id: int) -> bool:
        return node_id not in self.node_ids

    def copy(self) -> "NodePath":
        result = NodePath()
        result.path = self.path[:]
        result.node_ids = self.node_ids.copy()
        result.path_length = self.path_length
        return result

    def add(self, node_id: int, cost: int = 0) -> None:
        self.path.append(node_id)
        self.node_ids.add(node_id)
        self.path_length += cost

    def last(self) -> int:
        return self.path[-1]

    def __str__(self) -> str:
        return f"{self.path_length}, {self.node_ids}"

    def __len__(self) -> int:
        return self.path_length


class Solver2(Solver):
    maze: Maze

    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def get_cell_branches(self, position: Position) -> int:
        result = 0
        if self.maze[position] != ".":
            return 0
        for direction in position.expand():
            tile = self.maze[direction]
            if tile is not None and tile != "#":
                result += 1
        return result

    def get_nodes(self) -> dict[Position, Node]:
        nodes: list[Node] = []

        start = Position(0, 1)
        nodes.append(Node(0, start))
        name = 1
        for row in range(self.maze.num_rows):
            for col in range(self.maze.num_cols):
                pos = Position(row, col)
                if self.get_cell_branches(pos) > 2:
                    node = Node(name, pos)
                    name += 1
                    nodes.append(node)

        # add start and end coz they are dumb

        end = Position(self.maze.num_rows - 1, self.maze.num_cols - 2)

        nodes.append(Node(name, end))
        for node in nodes:
            self.maze[node.position] = colorama.Back.GREEN + "X" + colorama.Back.BLACK
        return {node.position: node for node in nodes}

    def fill_node(self, start_node: Node, nodes: dict[Position, Node]) -> None:
        first_path = Path()
        first_path.add(start_node.position)
        paths: Queue[Path] = Queue()
        paths.put(first_path)
        while not paths.empty():
            path = paths.get()
            pos = path.last()
            if pos != start_node.position and pos in nodes:
                # reached an edge
                edge = Edge(start_node.name, nodes[pos].name, path)
                start_node.edges.append(edge)
                end_node = nodes[pos]
                end_node.edges.append(edge.flip())
                continue
            expansions = self.expand_path(path)
            for path in expansions:
                paths.put(path)

    def expand_path(self, path: Path) -> list[Path]:
        current_pos: Position = path.last()
        expansions = current_pos.expand()

        valid_expansions = []
        for expansion in expansions:
            expansion_tile = self.maze[expansion]
            if (
                path.can_add(expansion)
                and expansion_tile is not None
                and expansion_tile != "#"
            ):
                valid_expansions.append(expansion)
                if expansion_tile == ".":
                    self.maze[expansion] = "#"

        if len(valid_expansions) == 0:
            return []
        elif len(valid_expansions) == 1:
            path.add(valid_expansions[0])
            return [path]
        else:
            result = []
            for expansion in valid_expansions[1:]:
                new_path = path.copy()
                new_path.add(expansion)
                result.append(new_path)
            path.add(valid_expansions[0])
            result.append(path)

            return result

    def expand_node_path(
        self, node_path: NodePath, nodes: list[Node]
    ) -> list[NodePath]:
        last_node: Node = nodes[node_path.last()]
        result = []
        for edge in last_node.edges:
            target_node_id: int = edge.node2
            if node_path.can_add(target_node_id):
                to_add = node_path.copy()
                to_add.add(target_node_id, len(edge.path))
                result.append(to_add)
        return result

    def build_nodes(self) -> list[Node]:
        nodes: dict[Position, Node] = self.get_nodes()
        print(self.maze)
        for node in nodes.values():
            self.fill_node(node, nodes)

        return list(nodes.values())

    def solve(self) -> list[BasePath]:
        nodes: list[Node] = self.build_nodes()
        first_path = NodePath()
        first_path.add(0)
        paths: Queue[NodePath] = Queue()
        paths.put(first_path)
        print("\n".join(str(node) for node in nodes))
        last = time.time()
        results: list[BasePath] = []
        count = 0
        while not paths.empty():
            path: NodePath = paths.get()
            node_id: int = path.last()
            if node_id == nodes[-1].name:  # end node
                # reached an edge
                count += 1
                results.append(path)
                if count % 10000 == 0:
                    print(paths.qsize(), path, time.time() - last)
                    last = time.time()
                continue
            expansions = self.expand_node_path(path, nodes)
            for path in expansions:
                paths.put(path)

        results.sort(key=lambda x: len(x), reverse=True)

        return results
