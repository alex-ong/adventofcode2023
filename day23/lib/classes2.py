"""part 2 solution"""
from dataclasses import dataclass, field
from queue import Queue

import colorama

from day23.lib.classes import Maze, Path, Position, Solver


# first simplify graph to "nodes", then brute force that.
@dataclass
class Node:
    name: int
    position: Position
    edges: list["Edge"] = field(default_factory=list)

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
            self.maze[node.position] = (
                colorama.Back.GREEN + str(node.name) + colorama.Back.BLACK
            )
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

    def solve(self) -> list[Path]:
        nodes: dict[Position, Node] = self.get_nodes()
        print(self.maze)
        for node in nodes.values():
            self.fill_node(node, nodes)

        for node in nodes.values():
            print(node)

        return []
