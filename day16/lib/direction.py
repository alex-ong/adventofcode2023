"""Direction class."""
from enum import IntEnum


class Direction(IntEnum):
    """Simple direction enum."""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __str__(self) -> str:
        """Return ``NORTH`` etc."""
        return self.name

    def opposite(self) -> "Direction":
        """Returns opposite direction."""
        int_value = int(self)
        return Direction((int_value + 2) % len(Direction))

    def offset(self, row: int, col: int) -> tuple[int, int]:
        """Offset a row/col by our direction."""
        if self == Direction.NORTH:
            return (row - 1, col)
        if self == Direction.EAST:
            return (row, col + 1)
        if self == Direction.SOUTH:
            return (row + 1, col)
        if self == Direction.WEST:
            return (row, col - 1)
        raise AssertionError("direction not suppported", self)
