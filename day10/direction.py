"""direction class"""
from enum import Enum


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4
    NORTH_EAST = 5
    NORTH_WEST = 6
    SOUTH_EAST = 7
    SOUTH_WEST = 8

    def opposite(self) -> "Direction":
        if self == Direction.NORTH:
            return Direction.SOUTH
        if self == Direction.SOUTH:
            return Direction.NORTH
        if self == Direction.EAST:
            return Direction.WEST
        if self == Direction.WEST:
            return Direction.EAST
        raise RuntimeError("invalid direction")