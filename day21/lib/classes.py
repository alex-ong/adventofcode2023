"""classes"""


from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


@dataclass
class Position:
    row: int
    col: int

    def __str__(self) -> str:
        return f"{self.row}, {self.col}"

    def __hash__(self) -> int:
        return hash(f"{self.row}, {self.col}")


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
        row = row if row is not None else self.row
        col = col if col is not None else self.col
        distance = distance if distance is not None else self.distance + 1
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

    def __getitem__(self, position: Position, wrap: bool = True) -> Optional[str]:
        """Get item via position. Returns None if out of bounds"""
        if not isinstance(position, Position):
            raise ValueError(f"position is not a Position, {type(position)}")
        if not wrap and self.is_oob(position):
            return None
        row = position.row % self.num_rows
        col = position.col % self.num_cols
        return self.grid[row][col]

    def is_oob(self, position: Position) -> bool:
        """true if position is out of bounds"""
        return (
            position.row < 0
            or position.row >= self.num_rows
            or position.col < 0
            or position.col >= self.num_cols
        )


class BaseDistanceMaze(ABC):
    def overlay(self, maze: Maze) -> str:
        return ""

    def calc_steps(self) -> int:
        return 0

    def __setitem__(self, position: Position, value: int) -> None:
        raise NotImplementedError()

    def __getitem__(self, position: Position) -> Optional[int]:
        raise NotImplementedError()


class DistanceMaze(BaseDistanceMaze):
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

    def overlay(self, maze: Maze) -> str:
        new_strings: list[str] = []
        base_str: str = str(self)

        for row, line in enumerate(base_str.split("\n")):
            other_str = maze.grid[row]
            my_str = ""
            for col, value in enumerate(line):
                if value == "_":
                    my_str += other_str[col]
                # elif value in "02468":
                #    my_str += value
                # else:
                #    my_str += "."
                else:
                    my_str += value
            new_strings.append(my_str)
        return "\n".join(new_strings)


class DistanceMazes(BaseDistanceMaze):
    grid: dict[Position, DistanceMaze]

    rows_per_maze: int
    cols_per_maze: int

    def __init__(self, num_rows: int, num_cols: int):
        self.rows_per_maze = num_rows
        self.cols_per_maze = num_cols
        self.grid = defaultdict(lambda: DistanceMaze(num_rows, num_cols))

    def __getitem__(self, position: Position) -> int:
        big_pos, sub_pos = self.get_split_pos(position)

        result = self.grid[big_pos][sub_pos]
        if result is None:
            raise ValueError("Unexpected result, None")
        return result

    def __setitem__(self, position: Position, value: int) -> None:
        if not isinstance(position, Position):
            raise ValueError(f"position is not a Position, {type(position)}")
        big_pos, sub_pos = self.get_split_pos(position)
        self.grid[big_pos][sub_pos] = value

    def get_split_pos(self, position: Position) -> tuple[Position, Position]:
        big_grid_row: int = position.row // self.rows_per_maze
        big_grid_col: int = position.col // self.cols_per_maze

        sub_grid_row: int = position.row % self.rows_per_maze
        sub_grid_col: int = position.col % self.cols_per_maze
        big_pos = Position(big_grid_row, big_grid_col)
        sub_pos = Position(sub_grid_row, sub_grid_col)
        return big_pos, sub_pos

    def overlay(self, maze: Maze) -> str:
        coords = list(self.grid.keys())
        rows = sorted([coord.row for coord in coords])
        cols = sorted([coord.col for coord in coords])

        if len(rows) == 0:
            min_row, max_row, min_col, max_col = 0, 0, 0, 0
        else:
            min_row, max_row = rows[0], rows[-1]
            min_col, max_col = cols[0], cols[-1]

        result = ""
        for big_row in range(min_row, max_row + 1):
            grids = []
            for big_col in range(min_col, max_col + 1):
                sub_grid: DistanceMaze = self.grid[Position(big_row, big_col)]
                grids.append(sub_grid.overlay(maze))

            grid_splits = [grid.split("\n") for grid in grids]

            row_lines = "\n".join(" ".join(lines) for lines in zip(*grid_splits))
            result += row_lines
            result += "\n\n"
        return result
