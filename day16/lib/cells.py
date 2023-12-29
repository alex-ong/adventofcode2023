"""Cell classes."""
from abc import ABC, abstractmethod

from day16.lib.direction import Direction
from day16.lib.laser import Laser


class Cell(ABC):
    """Abstract cell class."""

    contents: str

    @staticmethod
    def construct(contents: str) -> "Cell":
        """Construct proper cell from given contents."""
        if contents == ".":
            return DotCell()
        elif contents == "|":
            return PipeCell()
        elif contents == "-":
            return DashCell()
        elif contents == "/":
            return ForwardSlashCell()
        elif contents == "\\":
            return BackSlashCell()
        raise AssertionError(f"unrecognized content {contents}")

    @abstractmethod
    def next_lasers(self, laser: Laser) -> list[Laser]:
        """Return next lasers given a laser entering this cell."""
        raise AssertionError("Not supported", laser)


class DotCell(Cell):
    """A dot cell."""

    def __init__(self) -> None:
        """Sets our contents to ``.``."""
        self.contents = "."

    def next_lasers(self, laser: Laser) -> list[Laser]:
        """Lasers pass directly through this tile."""
        row, col = laser.direction.offset(laser.row, laser.col)
        return [Laser(row, col, laser.direction)]


class DashCell(Cell):
    """A ``-`` cell."""

    def __init__(self) -> None:
        """Sets our contents to ``-``."""
        self.contents = "-"

    def next_lasers(self, laser: Laser) -> list[Laser]:
        """Lasers must end up going east/west after passing through this cell."""
        if laser.direction in [Direction.EAST, Direction.WEST]:
            row, col = laser.direction.offset(laser.row, laser.col)
            return [Laser(row, col, laser.direction)]
        elif laser.direction in [Direction.NORTH, Direction.SOUTH]:
            row, col = laser.row, laser.col
            return [
                Laser(row, col + 1, Direction.EAST),
                Laser(row, col - 1, Direction.WEST),
            ]
        raise AssertionError(f"Unknown direction {laser.direction}")


class PipeCell(Cell):
    """A ``|`` cell."""

    def __init__(self) -> None:
        """Sets our contents to ``|``."""
        self.contents = "|"

    def next_lasers(self, laser: Laser) -> list[Laser]:
        """Lasers must end up going north/south after passing through this cell."""
        if laser.direction in [Direction.NORTH, Direction.SOUTH]:
            row, col = laser.direction.offset(laser.row, laser.col)
            return [Laser(row, col, laser.direction)]
        elif laser.direction in [Direction.EAST, Direction.WEST]:
            row, col = laser.row, laser.col
            return [
                Laser(row - 1, col, Direction.NORTH),
                Laser(row + 1, col, Direction.SOUTH),
            ]
        raise AssertionError(f"Unknown direction {laser.direction}")


class ForwardSlashCell(Cell):
    """A ``/`` cell."""

    def __init__(self) -> None:
        """Sets our contents to ``/``."""
        self.contents = "/"

    def next_lasers(self, laser: Laser) -> list[Laser]:
        """Lasers go diagonal mode."""
        row, col = laser.row, laser.col
        if laser.direction == Direction.EAST:
            return [Laser(row - 1, col, Direction.NORTH)]
        if laser.direction == Direction.NORTH:
            return [Laser(row, col + 1, Direction.EAST)]
        if laser.direction == Direction.SOUTH:
            return [Laser(row, col - 1, Direction.WEST)]
        if laser.direction == Direction.WEST:
            return [Laser(row + 1, col, Direction.SOUTH)]
        raise AssertionError(f"Unknown direction {laser.direction}")


class BackSlashCell(Cell):
    r"""A ``\`` cell."""

    def __init__(self) -> None:
        r"""Sets our contents to ``\``."""
        self.contents = "\\"

    def next_lasers(self, laser: Laser) -> list[Laser]:
        """Lasers go diagonal mode."""
        row, col = laser.row, laser.col
        if laser.direction == Direction.EAST:
            return [Laser(row + 1, col, Direction.SOUTH)]
        if laser.direction == Direction.SOUTH:
            return [Laser(row, col + 1, Direction.EAST)]
        if laser.direction == Direction.NORTH:
            return [Laser(row, col - 1, Direction.WEST)]
        if laser.direction == Direction.WEST:
            return [Laser(row - 1, col, Direction.NORTH)]
        raise AssertionError(f"Unknown direction {laser.direction}")
