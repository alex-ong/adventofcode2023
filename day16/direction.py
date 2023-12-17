"""
Direction class
"""
from enum import IntEnum


class Direction(IntEnum):
    """Simple direction enum"""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __str__(self):
        return self.name

    def opposite(self) -> "Direction":
        int_value = int(self)
        return Direction((int_value + 2) % len(Direction))

    def offset(self, row, col) -> tuple[int, int]:
        if self == Direction.NORTH:
            return (row - 1, col)
        if self == Direction.EAST:
            return (row, col + 1)
        if self == Direction.SOUTH:
            return (row + 1, col)
        if self == Direction.WEST:
            return (row, col - 1)
        raise ValueError("direction not suppported", self)
