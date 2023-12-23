"""Direciotn class"""
from enum import Enum, IntEnum


class Direction(IntEnum):
    North = 0
    West = 1
    South = 2
    East = 3

    __str__ = Enum.__str__

    def rotate_ccw(self) -> "Direction":
        int_value = int(self)
        return Direction((int_value - 1 + len(Direction)) % len(Direction))

    def rotate_cw(self) -> "Direction":
        int_value = int(self)
        return Direction((int_value + 1) % len(Direction))
