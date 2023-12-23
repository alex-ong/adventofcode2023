from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Position:
    row: int
    col: int

    def copy_modify(
        self, row: Optional[int] = None, col: Optional[int] = None
    ) -> "Position":
        if row is None:
            row = self.row
        if col is None:
            col = self.col
        return Position(row, col)

    def __str__(self) -> str:
        return f"{self.row}, {self.col}"


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
