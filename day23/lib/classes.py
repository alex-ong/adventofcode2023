from copy import deepcopy
from dataclasses import dataclass
from queue import Queue
from typing import Any, Optional


@dataclass(frozen=True, slots=True)
class Position:
    row: int
    col: int

    def copy_modify(
        self, row: Optional[int] = None, col: Optional[int] = None
    ) -> "Position":
        """Copies us and offsets by the given offset"""
        if row is None:
            row = self.row
        else:
            row = self.row + row
        if col is None:
            col = self.col
        else:
            col = self.col + col
        return Position(row, col)

    def __str__(self) -> str:
        return f"{self.row}, {self.col}"

    def expand(self) -> list["Position"]:
        """Expand in 4 cardinal directions"""
        return [
            self.copy_modify(row=-1),
            self.copy_modify(row=+1),
            self.copy_modify(col=-1),
            self.copy_modify(col=+1),
        ]


class Path:
    route: list[Position]
    nodes: set[Position]

    def __init__(self) -> None:
        self.route = []
        self.nodes = set()

    def can_add(self, position: Position) -> bool:
        return position not in self.nodes

    def add(self, position: Position) -> None:
        self.route.append(position)
        self.nodes.add(position)

    def copy(self) -> "Path":
        result = Path()
        result.route = self.route[:]
        result.nodes = set(result.route)
        return result

    def flip(self) -> "Path":
        result = self.copy()
        result.route.reverse()
        return result

    def last(self) -> Position:
        if len(self.route) == 0:
            raise ValueError("Don't call last when i'm empty 4head")
        return self.route[-1]

    def overlay(self, maze: "Maze") -> str:
        base_str = str(maze)
        char_array: list[list[str]] = [list(line) for line in base_str.split("\n")]
        for node in self.route:
            char_array[node.row][node.col] = "O"
        return "\n".join("".join(char for char in row) for row in char_array)

    def __len__(self) -> int:
        """Length of path. Has to be -1 because problem is like that"""
        return len(self.route) - 1

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, Path):
            raise AssertionError("eq only works on Path")
        return self.route == other.route

    def __hash__(self) -> int:
        return hash(",".join(str(item) for item in self.route))


class Maze:
    grid: list[list[str]]  # 2d array of chars
    num_rows: int
    num_cols: int

    def __init__(self, data: list[list[str]]) -> None:
        self.grid = data
        self.num_rows = len(data)
        self.num_cols = len(data[0])

    def __str__(self) -> str:
        return "\n".join("".join(col for col in row) for row in self.grid)

    def __getitem__(self, position: Position) -> Optional[str]:
        """Get item via position. Returns None if out of bounds"""
        if not isinstance(position, Position):
            raise AssertionError(f"position is not a Position, {type(position)}")
        if self.is_oob(position):
            return None
        return self.grid[position.row][position.col]

    def __setitem__(self, position: Position, value: str) -> None:
        """Get item via position. Returns None if out of bounds"""
        if not isinstance(position, Position):
            raise AssertionError(f"position is not a Position, {type(position)}")
        if self.is_oob(position):
            raise AssertionError("can't set outside our maze!")
        self.grid[position.row][position.col] = value

    def is_oob(self, position: Position) -> bool:
        """True if position is out of bounds"""
        return (
            position.row < 0
            or position.row >= self.num_rows
            or position.col < 0
            or position.col >= self.num_cols
        )

    def copy(self) -> "Maze":
        result = Maze(deepcopy(self.grid))
        return result

    def get_cell_branches(self, position: Position) -> int:
        """Returns how many branches come out of this tile"""
        result = 0
        if self[position] != ".":
            return 0
        for direction in position.expand():
            tile = self[direction]
            if tile is not None and tile != "#":
                result += 1
        return result


class Solver1:
    maze: Maze
    handle_hills: bool

    def __init__(self, maze: Maze, handle_hills: bool = True) -> None:
        self.maze = maze
        self.handle_hills = handle_hills

    def solve(self) -> list[Path]:
        paths: Queue[Path] = Queue()
        first_path = Path()
        first_path.add(Position(0, 1))
        paths.put(first_path)
        # bfs all paths simultaneously
        results: list[Path] = []
        count = 1
        while not paths.empty():
            path = paths.get()
            if path.last().row == self.maze.num_rows - 1:
                results.append(path)
                continue

            expansions = self.expand_path(path)
            for expansion in expansions:
                paths.put(expansion)
            count += 1

        return results

    def expand_hill(self, position: Position, tile: str) -> list[Position]:
        if tile == "^":
            return [position.copy_modify(row=-1)]
        elif tile == "v":
            return [position.copy_modify(row=+1)]
        elif tile == "<":
            return [position.copy_modify(col=-1)]
        elif tile == ">":
            return [position.copy_modify(col=+1)]
        else:
            return position.expand()

    def expand_path(self, path: Path) -> list[Path]:
        current_pos: Position = path.last()
        current_tile: Optional[str] = self.maze[current_pos]
        if current_tile is None:
            raise AssertionError("there's no shot we got a tile outside the maze")
        expansions: list[Position]
        if self.handle_hills:
            expansions = self.expand_hill(current_pos, current_tile)
        else:
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
        return generate_paths(path, valid_expansions)


def generate_paths(path: Path, expansions: list[Position]) -> list[Path]:
    """Given a path and valid expansions, (optionally) copies the path.
    Returns a list of new paths. If there is only one expansion, modifies it
    in-place
    """
    if len(expansions) == 0:
        return []
    elif len(expansions) == 1:
        path.add(expansions[0])
        return [path]
    else:
        result = []
        for expansion in expansions[1:]:
            new_path = path.copy()
            new_path.add(expansion)
            result.append(new_path)
        path.add(expansions[0])
        result.append(path)

        return result
