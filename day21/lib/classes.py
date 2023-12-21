"""classes"""


from dataclasses import dataclass
from typing import Optional


@dataclass
class Position:
    row: int
    col: int

    def __str__(self) -> str:
        return f"{self.row}, {self.col}"


@dataclass(kw_only=True)
class PositionDist(Position):
    distance: int

    def __str__(self) -> str:
        return f"{self.row}, {self.col}, d={self.distance}"

    def replace(
        self,
        row: Optional[int] = None,
        col: Optional[int] = None,
        distance: Optional[int] = None,
    ) -> "PositionDist":
        """
        return a copy with given args changed
        Distance will +1 if not supplied
        """
        row = row or self.row
        col = col or self.col
        distance = distance or self.distance + 1
        return PositionDist(row, col, distance=distance)


class Maze:
    grid: list[str]

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


class DistanceMaze:
    grid: list[list[int]]
    num_rows: int
    num_cols: int

    def __init__(self, num_rows: int, num_cols: int) -> None:
        self.num_rows = num_rows
        self.num_cols = num_cols

        self.grid = [[-1 for _ in range(num_cols)] for _ in range(num_rows)]

    def __setitem__(self, position: Position, value: int) -> None:
        """Sets item at given position. Silently fails if out of bounds"""
        if not isinstance(position, Position):
            raise ValueError(f"position is not a Position, {type(position)}")
        if self.is_oob(position):
            return
        self.grid[position.row][position.col] = value

    def __getitem__(self, position: Position) -> Optional[int]:
        """Get item via position. Returns None if out of bounds"""
        if not isinstance(position, Position):
            raise ValueError(f"position is not a Position, {type(position)}")
        if self.is_oob(position):
            return None
        return self.grid[position.row][position.col]

    def __str__(self) -> str:
        return "\n".join(
            "".join(self.int_to_str(col) for col in row) for row in self.grid
        )

    def is_oob(self, position: Position) -> bool:
        """true if position is out of bounds"""
        return (
            position.row < 0
            or position.row >= self.num_rows
            or position.col < 0
            or position.col >= self.num_cols
        )

    def int_to_str(self, value: int) -> str:
        if value == -1:
            return "_"
        return str(value)[-1]

    def calc_steps(self) -> int:
        result = 0
        for row in self.grid:
            result += sum(1 if item % 2 == 0 else 0 for item in row)
        return result
