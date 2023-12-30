"""part 2 solution."""
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor as Pool
from dataclasses import dataclass, field
from queue import Queue
from typing import Any

import colorama

from day23.lib import classes
from day23.lib.classes import Maze, Path, Position

colorama.init(convert=True)


@dataclass(eq=True)
class Node:
    """Node representing a fork to another."""

    name: int = field(compare=True)
    position: Position = field(compare=False)
    edges: list["Edge"] = field(default_factory=list, repr=False, compare=False)

    def __str__(self) -> str:
        """Pretty-print."""
        return f"{self.name}: ({self.position}) {[str(edge) for edge in self.edges]}"


@dataclass
class Edge:
    """Edge class, representing a path between nodes."""

    node1: int
    node2: int
    path: Path = field(repr=False)
    length: int = 0

    def __post_init__(self) -> None:
        """Cache our length."""
        self.length = len(self.path)

    def flip(self) -> "Edge":
        """Reverse a path."""
        return Edge(self.node2, self.node1, self.path.flip())

    def __str__(self) -> str:
        """Pretty-print."""
        return f"{self.node1}->{self.node2}, {self.length}"


class Solver2:
    """Solver for part 2."""

    input_maze: Maze

    def __init__(self, maze: Maze) -> None:
        """Store maze that we need to solve."""
        self.input_maze = maze

    @staticmethod
    def get_nodes(maze: Maze) -> dict[Position, Node]:
        """Gets nodes and marks them on the given maze.

        Note that the maze is modified in-place!
        Nodes are *not* populated with edges
        """
        nodes: list[Node] = []

        start = Position(0, 1)
        nodes.append(Node(0, start))
        name = 1
        for row in range(maze.num_rows):
            for col in range(maze.num_cols):
                pos = Position(row, col)
                if maze.get_cell_branches(pos) > 2:
                    node = Node(name, pos)
                    name += 1
                    nodes.append(node)

        # add start and end coz they are dumb
        end = Position(maze.num_rows - 1, maze.num_cols - 2)
        nodes.append(Node(name, end))

        for node in nodes:
            maze[node.position] = colorama.Back.GREEN + "X" + colorama.Back.BLACK
        return {node.position: node for node in nodes}

    @staticmethod
    def calculate_edges(
        start_node: Node, nodes: dict[Position, Node], maze: Maze
    ) -> None:
        """Calculate edges of the maze.

        Modifies the maze inplace, filling it in with #.
        Modifies the node and its connecting nodes by adding Edges
        """
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
            expansions = Solver2.expand_path(path, maze)
            for path in expansions:
                paths.put(path)

    @staticmethod
    def expand_path(path: Path, maze: Maze) -> list[Path]:
        """Expands a path, nuking that section of the maze using #."""
        current_pos: Position = path.last()
        expansions = current_pos.expand()

        valid_expansions = []
        for expansion in expansions:
            expansion_tile = maze[expansion]
            if (
                path.can_add(expansion)
                and expansion_tile is not None
                and expansion_tile != "#"
            ):
                valid_expansions.append(expansion)
                if expansion_tile == ".":
                    maze[expansion] = "#"
        return classes.generate_paths(path, valid_expansions)

    def build_nodes(self) -> list[Node]:
        """Build nodes and edges on a copy of the maze."""
        # make backup of maze
        maze_copy = self.input_maze.copy()
        nodes: dict[Position, Node] = self.get_nodes(maze_copy)
        print(maze_copy)
        for node in nodes.values():
            self.calculate_edges(node, nodes, maze_copy)

        return list(nodes.values())

    def solve(self) -> int:
        """Solves the maze."""
        nodes: list[Node] = self.build_nodes()

        print("\n".join(str(node) for node in nodes))
        start = time.time()
        cpu_count = os.cpu_count() or 2
        levels = int(math.log(cpu_count, 2))
        result = solve2(nodes, 0, len(nodes) - 1, 0, set(), levels)
        print(f"Executed in: {time.time() - start}")
        return result


def solve2(
    nodes: list[Node],
    current: int,
    destination: int,
    distance: int,
    seen: set[int],
    forks_remaining: int,
) -> int:
    """Solves a dfs by creating forking into multiprocessing."""
    if current == destination:
        return distance

    best = 0
    seen.add(current)

    # run the code in this thread
    if forks_remaining == 0 or len(nodes[current].edges) == 1:
        for edge in nodes[current].edges:
            neighbor, weight = edge.node2, edge.length
            if neighbor in seen:
                continue

            result = solve2(
                nodes,
                neighbor,
                destination,
                distance + weight,
                seen,
                forks_remaining,
            )
            best = max(best, result)
    else:  # Use multiprocessing.Pool for parallel execution
        tasks = []
        for edge in nodes[current].edges:
            neighbor, weight = edge.node2, edge.length
            if neighbor in seen:
                continue
            tasks.append(
                [
                    nodes,
                    neighbor,
                    destination,
                    distance + weight,
                    seen,
                    forks_remaining - 1,
                ]
            )
        with Pool(len(tasks)) as pool:
            for result in pool.map(solve2_helper, tasks):
                best = max(best, result)

    seen.remove(current)

    return best


def solve2_helper(args: list[Any]) -> int:
    """ThreadPoolExecutor doesnt have starmap so we use a helper."""
    return solve2(*args)
