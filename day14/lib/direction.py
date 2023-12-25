"""Direciotn class"""
from enum import Enum, IntEnum


class Direction(IntEnum):
    North = 0
    West = 1
    South = 2
    East = 3

    __str__ = Enum.__str__

    def next_direction_cw(self) -> "Direction":
        """if we are pointing west, the next direction clockwise is north"""
        int_value = int(self)
        return Direction((int_value - 1 + len(Direction)) % len(Direction))

    def next_direction_ccw(self) -> "Direction":
        """if we are pointing west, the next direction ccw is south"""
        int_value = int(self)
        return Direction((int_value + 1) % len(Direction))
