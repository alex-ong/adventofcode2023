"""classes for day21."""


from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from colorama import Back


@dataclass(unsafe_hash=True)
class Position:
    """Simple 2d vector.

    It implements an unsafe hash since PositionDist inherits from this.
    """

    row: int
    col: int

    def __str__(self) -> str:
        """Prettyprint position."""
        return f"{self.row}, {self.col}"


@dataclass(kw_only=True)
class PositionDist(Position):
    """Position + distance."""

    distance: int

    def __str__(self) -> str:
        """Pretty-print."""
        return f"{self.row}, {self.col}, d={self.distance}"

    def replace(
        self,
        row: Optional[int] = None,
        col: Optional[int] = None,
        distance: Optional[int] = None,
    ) -> "PositionDist":
        """Return a copy with given args changed.

        Distance will +1 if not supplied
        """
        row = row if row is not None else self.row
        col = col if col is not None else self.col
        distance = distance if distance is not None else self.distance + 1
        return PositionDist(row, col, distance=distance)


class Maze:
    """2d grid of items."""

    grid: list[str]

    num_rows: int
    num_cols: int

    def __init__(self, data: list[str]) -> None:
        """Constructs maze from list of strings."""
        self.grid = data
        self.num_rows = len(data)
        self.num_cols = len(data[0])

    def __str__(self) -> str:
        """Pretty-print."""
        return "\n".join(row for row in self.grid)

    def __getitem__(self, position: Position) -> Optional[str]:
        """Get item via position. Always wraps."""
        if not isinstance(position, Position):
            raise AssertionError(f"position is not a Position, {type(position)}")

        row = position.row % self.num_rows
        col = position.col % self.num_cols
        return self.grid[row][col]


class BaseDistanceMaze(ABC):
    """Abstract distance maze."""

    @abstractmethod
    def overlay(self, maze: Maze) -> str:
        """Overlays on top of a maze."""
        raise AssertionError("Not implemented")

    @abstractmethod
    def calc_steps(self, remainder: int) -> int:
        """Calculate steps.

        Matches remainder == 1 or remainder == 0
        When modulo'ing by 2
        """

    @abstractmethod
    def __setitem__(self, position: Position, value: int) -> None:
        """Sets the 2d arrays value based on a position."""

    @abstractmethod
    def __getitem__(self, position: Position) -> Optional[int]:
        """Get the integer distance based on position."""


class DistanceMaze(BaseDistanceMaze):
    """Distance Maze == Maze.size."""

    grid: list[list[int]]
    num_rows: int
    num_cols: int

    def __init__(self, num_rows: int, num_cols: int) -> None:
        """Creates empty distance maze."""
        self.num_rows = num_rows
        self.num_cols = num_cols

        self.grid = [[-1 for _ in range(num_cols)] for _ in range(num_rows)]

    def __setitem__(self, position: Position, value: int) -> None:
        """Sets item at given position. Silently fails if out of bounds."""
        if not isinstance(position, Position):
            raise AssertionError(f"position is not a Position, {type(position)}")
        if self.is_oob(position):
            return
        self.grid[position.row][position.col] = value

    def __getitem__(self, position: Position) -> Optional[int]:
        """Get item via position. Returns None if out of bounds."""
        if not isinstance(position, Position):
            raise AssertionError(f"position is not a Position, {type(position)}")
        if self.is_oob(position):
            return None
        return self.grid[position.row][position.col]

    def __str__(self) -> str:
        """Prettyprint distance maze."""
        return "\n".join(
            "".join(self.int_to_str(col) for col in row) for row in self.grid
        )

    def is_oob(self, position: Position) -> bool:
        """True if position is out of bounds."""
        return (
            position.row < 0
            or position.row >= self.num_rows
            or position.col < 0
            or position.col >= self.num_cols
        )

    def int_to_str(self, value: int) -> str:
        """Convert integert to string."""
        if value == -1:
            return "_"
        return str(value)[-1]

    def calc_steps(self, remainder: int) -> int:
        """Calculate steps, based on odd/even steps."""

        def is_valid(val: int) -> bool:
            return val % 2 == remainder and val >= 0

        result = 0
        for row in self.grid:
            result += sum(1 if is_valid(item) else 0 for item in row)
        return result

    def overlay(self, maze: Maze) -> str:
        """Overlay this distance_maze on a maze."""
        new_strings: list[str] = []
        base_str: str = str(self)
        is_complete = self.is_complete()
        for row, line in enumerate(base_str.split("\n")):
            other_str = maze.grid[row]
            my_str = ""
            for col, value in enumerate(line):
                if is_complete and self.centre_cell(row, col):
                    if value in "02468":
                        my_str += Back.GREEN + value + Back.BLACK
                    else:
                        my_str += Back.RED + value + Back.BLACK
                elif value == "_":
                    my_str += other_str[col]
                else:
                    my_str += value

            new_strings.append(my_str)
        return "\n".join(new_strings)

    def centre_cell(self, row: int, col: int) -> bool:
        """Returns true if coordinate is the centre cell of the maze."""
        return row == self.num_rows // 2 and col == self.num_cols // 2

    def is_complete(self) -> bool:
        """Returns true if all cells are filled."""
        return (
            self.grid[0][0] != -1
            and self.grid[0][-1] != -1
            and self.grid[-1][0] != -1
            and self.grid[-1][-1] != -1
        )


class DistanceMazes(BaseDistanceMaze):
    """An array of distance mazes, able to extend infinitely."""

    grid: dict[Position, DistanceMaze]

    rows_per_maze: int
    cols_per_maze: int

    def __init__(self, num_rows: int, num_cols: int):
        """Initializes a growable 2d array of mazes."""
        self.rows_per_maze = num_rows
        self.cols_per_maze = num_cols
        self.grid = defaultdict(lambda: DistanceMaze(num_rows, num_cols))

    def get_big_grid(self, position: Position) -> DistanceMaze:
        """Big grid coordinate."""
        return self.grid[position]

    def __getitem__(self, position: Position) -> int:
        """Global coordinate 0 .. ± infinity."""
        big_pos, sub_pos = self.get_split_pos(position)

        result = self.grid[big_pos][sub_pos]
        if result is None:
            raise AssertionError("Unexpected result, None")
        return result

    def __setitem__(self, position: Position, value: int) -> None:
        """Sets a position's value."""
        if not isinstance(position, Position):
            raise AssertionError(f"position is not a Position, {type(position)}")
        big_pos, sub_pos = self.get_split_pos(position)
        self.grid[big_pos][sub_pos] = value

    def get_split_pos(self, position: Position) -> tuple[Position, Position]:
        """Split global position.

        Into big map and small map positions.

        Args:
            position (Position): global position

        Returns:
            tuple[Position, Position]: big coord, small coord
        """
        big_grid_row: int = position.row // self.rows_per_maze
        big_grid_col: int = position.col // self.cols_per_maze

        sub_grid_row: int = position.row % self.rows_per_maze
        sub_grid_col: int = position.col % self.cols_per_maze
        big_pos = Position(big_grid_row, big_grid_col)
        sub_pos = Position(sub_grid_row, sub_grid_col)
        return big_pos, sub_pos

    def overlay(self, maze: Maze) -> str:
        """Overlay our gigamap onto a maze."""
        coords = list(self.grid.keys())
        rows = sorted([coord.row for coord in coords])
        cols = sorted([coord.col for coord in coords])

        if len(rows) == 0:
            raise AssertionError("grid has no subgrids!")
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

    def calc_steps(self, remainder: int) -> int:
        """Calculate steps given parity."""
        distance_mazes = self.grid.values()
        result = sum(sub_grid.calc_steps(remainder) for sub_grid in distance_mazes)
        return result


class GiantNodeType(Enum):
    """A bunch of giant node types.

    turn each "maze" into a node type.
    assume parity == EVEN
    e.g. 9 x 9 maze matrix
    mazes_center_to_bottom == 9 //2 == 4

    BIG -> mazes_center_to_bottom - 1 == 3
    SMALL -> mazes_center_to_bottom == 4
    FULL_EVEN -> (mazes_center_to_bottom-1) ^2 == 9
    FULL_ODD -> mazes_center_to_bottom^2 == 16
    """

    FULL_EVEN = 0  # same as start tile
    FULL_ODD = 1  # 1 away from start tile
    NORTH_TIP = 2
    NORTH_EAST_BIG = 3
    NORTH_EAST_SMALL = 4
    EAST_TIP = 5
    SOUTH_EAST_BIG = 6
    SOUTH_EAST_SMALL = 7
    SOUTH_TIP = 8
    SOUTH_WEST_BIG = 9
    SOUTH_WEST_SMALL = 10
    WEST_TIP = 11
    NORTH_WEST_BIG = 12
    NORTH_WEST_SMALL = 13


class GiantNodeParser:
    """Convert from mazes to giant nodes."""

    distance_mazes: DistanceMazes
    full_edge_dist: int
    edge_dist: int

    def __init__(self, distance_mazes: DistanceMazes, nodes_to_edge: int) -> None:
        """Initialize Parser.

        e.g. 5x5, with steps == 10+2
        nodes_to_edge == 2
        5x5, steps == 15+2
        nodes_to_edge == 3
        """
        if nodes_to_edge < 3:
            raise ValueError("this shit only works with at least 3 bignodes!")
        self.distance_mazes = distance_mazes
        self.full_edge_dist = nodes_to_edge  # edge dist of mega map
        self.edge_dist = max(pos.row for pos in distance_mazes.grid)
        print("nodes_to_edge", nodes_to_edge)
        print("calculated_nodes_to_edge", self.edge_dist)

    def get_node(self, node_type: GiantNodeType) -> DistanceMaze:  # noqa: C901
        """Returns a giant node given its type."""
        if node_type == GiantNodeType.FULL_EVEN:
            return self.distance_mazes.get_big_grid(Position(0, 0))
        elif node_type == GiantNodeType.FULL_ODD:
            return self.distance_mazes.get_big_grid(Position(0, 1))
        elif node_type == GiantNodeType.NORTH_TIP:
            return self.distance_mazes.get_big_grid(Position(-self.edge_dist, 0))
        elif node_type == GiantNodeType.NORTH_EAST_BIG:
            return self.distance_mazes.get_big_grid(Position(-self.edge_dist + 1, 1))
        elif node_type == GiantNodeType.NORTH_EAST_SMALL:
            return self.distance_mazes.get_big_grid(Position(-self.edge_dist, 1))
        elif node_type == GiantNodeType.EAST_TIP:
            return self.distance_mazes.get_big_grid(Position(0, self.edge_dist))
        elif node_type == GiantNodeType.SOUTH_EAST_BIG:
            return self.distance_mazes.get_big_grid(Position(1, self.edge_dist - 1))
        elif node_type == GiantNodeType.SOUTH_EAST_SMALL:
            return self.distance_mazes.get_big_grid(Position(1, self.edge_dist))
        elif node_type == GiantNodeType.SOUTH_TIP:
            return self.distance_mazes.get_big_grid(Position(self.edge_dist, 0))
        elif node_type == GiantNodeType.SOUTH_WEST_BIG:
            return self.distance_mazes.get_big_grid(Position(self.edge_dist - 1, -1))
        elif node_type == GiantNodeType.SOUTH_WEST_SMALL:
            return self.distance_mazes.get_big_grid(Position(self.edge_dist, -1))
        elif node_type == GiantNodeType.WEST_TIP:
            return self.distance_mazes.get_big_grid(Position(0, -self.edge_dist))
        elif node_type == GiantNodeType.NORTH_WEST_BIG:
            return self.distance_mazes.get_big_grid(Position(-1, -self.edge_dist + 1))
        elif node_type == GiantNodeType.NORTH_WEST_SMALL:
            return self.distance_mazes.get_big_grid(Position(-1, -self.edge_dist))
        raise AssertionError(f"Unknown node_type: {node_type}")

    def get_node_count(self, node_type: GiantNodeType) -> int:
        """Returns how many of the giant node are required."""
        remainder = self.full_edge_dist % 2
        if node_type == GiantNodeType.FULL_EVEN:
            if remainder == 0:
                return (self.full_edge_dist - 1) * (self.full_edge_dist - 1)
            else:  # odd_parity
                return self.full_edge_dist * self.full_edge_dist
        elif node_type == GiantNodeType.FULL_ODD:
            if remainder == 0:
                return self.full_edge_dist * self.full_edge_dist
            else:  # odd_parity
                return (self.full_edge_dist - 1) * (self.full_edge_dist - 1)
        elif node_type in [
            GiantNodeType.NORTH_TIP,
            GiantNodeType.EAST_TIP,
            GiantNodeType.WEST_TIP,
            GiantNodeType.SOUTH_TIP,
        ]:
            return 1
        elif node_type in [
            GiantNodeType.NORTH_EAST_BIG,
            GiantNodeType.NORTH_WEST_BIG,
            GiantNodeType.SOUTH_EAST_BIG,
            GiantNodeType.SOUTH_WEST_BIG,
        ]:
            return self.full_edge_dist - 1
        elif node_type in [
            GiantNodeType.NORTH_EAST_SMALL,
            GiantNodeType.NORTH_WEST_SMALL,
            GiantNodeType.SOUTH_EAST_SMALL,
            GiantNodeType.SOUTH_WEST_SMALL,
        ]:
            return self.full_edge_dist
        raise AssertionError(f"Unknown node type: {node_type}")
