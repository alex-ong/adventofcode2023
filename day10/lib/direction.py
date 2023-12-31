"""direction Enum."""
from enum import Enum


class Direction(Enum):
    """Cardinal (NSEW) direction Enum."""

    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

    def opposite(self) -> "Direction":
        """Return opposite direction.

        e.g. ``E``<->``W``
        and ``N``<->``S``

        Raises:
            AssertionError: if direction is invalid

        Returns:
            Direction: opposite direction.
        """
        if self == Direction.NORTH:
            return Direction.SOUTH
        if self == Direction.SOUTH:
            return Direction.NORTH
        if self == Direction.EAST:
            return Direction.WEST
        if self == Direction.WEST:
            return Direction.EAST
        raise AssertionError("invalid direction")
