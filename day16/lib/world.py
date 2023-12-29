"""Well defined world classes."""
from dataclasses import dataclass, field

from day16.lib.cells import Cell
from day16.lib.laser import Laser


class SolvedWorld:
    """A solved world class, stores how many lasers are in each tile."""

    data: list[list[list[Laser]]]

    def __init__(self, num_rows: int, num_cols: int):
        """Initialises empty 2d array of lists of lasers."""
        self.data = [[[] for _ in range(num_cols)] for _ in range(num_rows)]

    def already_solved(self, laser: Laser) -> bool:
        """Returns true if laser already calculated."""
        solutions = self.data[laser.row][laser.col]
        if laser in solutions:
            return True
        return False

    def add_laser(self, laser: Laser) -> None:
        """Adds laser to cell."""
        solutions = self.data[laser.row][laser.col]
        solutions.append(laser)

    def __str__(self) -> str:
        """Custom str to show how many lasers on each tile."""
        row_strs = []
        for row in self.data:
            row_str = "".join(str(len(col)) for col in row)
            row_strs.append(row_str)
        return "\n".join(row_strs)

    def num_energized(self) -> int:
        """Return number of energized cells."""
        result: int = 0
        for row in self.data:
            result += sum(1 if len(col) >= 1 else 0 for col in row)
        return result


@dataclass
class World:
    """The input world (mirrors/empty tiles)."""

    data: list[list[Cell]]

    num_rows: int = field(init=False, repr=False)
    num_cols: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Initializes our num_rows/num_cols."""
        self.num_rows = len(self.data)
        self.num_cols = len(self.data[0])

    def solve(self, start_laser: Laser) -> SolvedWorld:
        """Solve our world."""
        solved_world = SolvedWorld(self.num_rows, self.num_cols)
        active_lasers = [start_laser]
        while len(active_lasers) > 0:
            laser = active_lasers.pop(0)
            if self.is_oob(laser):
                continue
            if solved_world.already_solved(laser):
                continue
            solved_world.add_laser(laser)

            cell: Cell = self.data[laser.row][laser.col]
            next_lasers = cell.next_lasers(laser)
            active_lasers.extend(next_lasers)
        return solved_world

    def is_oob(self, laser: Laser) -> bool:
        """True if laser is out of bounds."""
        return (
            laser.row < 0
            or laser.row >= self.num_rows
            or laser.col < 0
            or laser.col >= self.num_cols
        )
