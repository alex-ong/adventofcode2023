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
