from dataclasses import dataclass
from typing import Optional


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
        """length of path. Has to be -1 because problem is like that"""
        return len(self.route) - 1


class Maze:
    grid: list[str]  # 2d array of chars
    num_rows: int
    num_cols: int

    def __init__(self, data: list[str]) -> None:
        self.grid = data
        self.num_rows = len(data)
        self.num_cols = len(data[0])

    def __str__(self) -> str:
        return "\n".join(row for row in self.grid)

    def __getitem__(self, position: Position) -> Optional[str]:
        """Get item via position. Returns None if out of bounds"""
        if not isinstance(position, Position):
            raise ValueError(f"position is not a Position, {type(position)}")
        if self.is_oob(position):
            return None
        return self.grid[position.row][position.col]

    def is_oob(self, position: Position) -> bool:
        """true if position is out of bounds"""
        return (
            position.row < 0
            or position.row >= self.num_rows
            or position.col < 0
            or position.col >= self.num_cols
        )
