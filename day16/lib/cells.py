"""Cell classes."""
from abc import ABC, abstractmethod
from typing import Callable, Dict, Type, TypeVar

from day16.lib.direction import Direction
from day16.lib.laser import Laser


class Cell(ABC):
    """Abstract cell class."""

    contents: str

    # each cell can register itself to us
    CELL_TYPES: Dict[str, Type["Cell"]] = {}

    def __init__(self, contents: str):
        """Default constructor, sets our contents."""
        self.contents = contents

    @staticmethod
    def register_cell_type(
        cell_contents: str,
    ) -> Callable[[type["Cell"]], type["Cell"]]:
        """Registers a cell type to this factory."""

        def decorator(cls: Type["Cell"]) -> Type["Cell"]:
            Cell.CELL_TYPES[cell_contents] = cls
            return cls

        return decorator

    @staticmethod
    def construct(contents: str) -> "Cell":
        """Construct proper cell from given contents."""
        try:
            return Cell.CELL_TYPES[contents](contents)
        except KeyError:
            raise AssertionError(f"unrecognized content {contents}")

    @abstractmethod
    def next_lasers(self, laser: Laser) -> list[Laser]:
        """Return next lasers given a laser entering this cell."""
        raise AssertionError("Not supported", laser)


@Cell.register_cell_type(".")
class DotCell(Cell):
    """A dot cell."""

    def next_lasers(self, laser: Laser) -> list[Laser]:
        """Lasers pass directly through this tile."""
        row, col = laser.direction.offset(laser.row, laser.col)
        return [Laser(row, col, laser.direction)]


@Cell.register_cell_type("-")
class DashCell(Cell):
    """A ``-`` cell."""

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


@Cell.register_cell_type("|")
class PipeCell(Cell):
    """A ``|`` cell."""

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


@Cell.register_cell_type("/")
class ForwardSlashCell(Cell):
    """A ``/`` cell."""

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


@Cell.register_cell_type("\\")
class BackSlashCell(Cell):
    r"""A ``\`` cell."""

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
