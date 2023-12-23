"""part 2 solution"""
from dataclasses import dataclass, field
from multiprocessing import Pool
from queue import Queue

import colorama
import tqdm

from day23.lib.classes import BasePath, Maze, Path, Position, Solver

colorama.init(convert=True)


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


def expand_node_path(node_path: NodePath, nodes: list[Node]) -> list[NodePath]:
    """Expands a node path, giving back a list of of NodePaths"""
    last_node: Node = nodes[node_path.last()]
    result = []
    for edge in last_node.edges:
        target_node_id: int = edge.node2
        if node_path.can_add(target_node_id):
            to_add = node_path.copy()
            to_add.add(target_node_id, len(edge.path))
            result.append(to_add)
    return result


def worker_solve(
    nodes: list[Node],
    paths_to_process: list[NodePath],
    break_early: bool,
    thread_id: int,
) -> tuple[list[BasePath], list[NodePath]]:
    results: list[BasePath] = []
    unfinished_paths: Queue[NodePath] = Queue()
    for item in paths_to_process:
        unfinished_paths.put(item)

    pbar = tqdm.tqdm(
        desc=f"Thread{thread_id}", total=len(paths_to_process), position=thread_id
    )
    if break_early:
        pbar.total = 10000
        pbar.set_description("Initial run")

    while not unfinished_paths.empty():
        path = unfinished_paths.get()
        node_id: int = path.last()
        if node_id == nodes[-1].name:  # end node
            results.append(path)

            if break_early:
                pbar.update()
                if pbar.n % 10000 == 0:
                    break

            continue

        expansions = expand_node_path(path, nodes)

        if not break_early:
            pbar.total += len(expansions)
            pbar.update()

        for p in expansions:
            unfinished_paths.put(p)
    pbar.close()
    return results, list(unfinished_paths.queue)


def split_list(items: list[NodePath], num_chunks: int) -> list[list[NodePath]]:
    chunk_size = (len(items) // num_chunks) + 1
    return [items[i * chunk_size : (i + 1) * chunk_size] for i in range(num_chunks)]


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

    def build_nodes(self) -> list[Node]:
        nodes: dict[Position, Node] = self.get_nodes()
        print(self.maze)
        for node in nodes.values():
            self.fill_node(node, nodes)

        return list(nodes.values())

    def solve(self) -> list[BasePath]:
        nodes: list[Node] = self.build_nodes()
        # print our nodes out:
        print("\n".join(str(node) for node in nodes))

        first_path = NodePath()
        first_path.add(0)

        unfinished_paths: list[NodePath] = []
        unfinished_paths.append(first_path)

        results, unfinished_paths = worker_solve(nodes, unfinished_paths, True, 0)

        # time for multithreading!
        num_workers = 8
        unfinished_chunks: list[list[NodePath]] = split_list(
            unfinished_paths, num_workers
        )

        with Pool(num_workers) as pool:
            worker_args = [
                (nodes, unfinished_chunks[i], False, i) for i in range(num_workers)
            ]
            result_objects = pool.starmap_async(worker_solve, worker_args)
            pool_results = result_objects.get()
            for pool_result in pool_results:
                paths = pool_result[0]
                results.extend(paths)
        print("\n" * num_workers * 2)  # fix bug in progress bars
        # split unfinished_paths:
        results.sort(key=lambda x: len(x), reverse=True)
        print("total results:", len(results))
        return results
