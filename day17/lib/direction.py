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

    def __str__(self) -> str:
        if self == Direction.NORTH:
            return "^"
        elif self == Direction.EAST:
            return ">"
        elif self == Direction.SOUTH:
            return "v"
        elif self == Direction.WEST:
            return "<"
        raise AssertionError("invalid value")

    def opposite(self) -> "Direction":
        int_value = int(self)
        return Direction((int_value + 2) % len(Direction))

    def offset(self, row: int, col: int) -> tuple[int, int]:
        if self == Direction.NORTH:
            return (row - 1, col)
        if self == Direction.EAST:
            return (row, col + 1)
        if self == Direction.SOUTH:
            return (row + 1, col)
        if self == Direction.WEST:
            return (row, col - 1)
        raise AssertionError("direction not suppported", self)

    def offset_list(self, row: int, col: int, size: int = 4) -> list[tuple[int, int]]:
        offsets = range(1, size + 1)
        if self == Direction.NORTH:
            return [(row - i, col) for i in offsets]
        if self == Direction.EAST:
            return [((row, col + i)) for i in offsets]
        if self == Direction.SOUTH:
            return [(row + i, col) for i in offsets]
        if self == Direction.WEST:
            return [(row, col - i) for i in offsets]
        raise AssertionError("direction not suppported", self)


ALL_DIRECTIONS = list(Direction)
