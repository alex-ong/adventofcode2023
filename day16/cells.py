"""
Cell classes
"""
from abc import ABC, abstractmethod

from direction import Direction
from laser import Laser


class Cell(ABC):
    contents: str

    @staticmethod
    def construct(contents: str) -> "Cell":
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
        raise ValueError(f"unrecognized content {contents}")

    def __init__(self, contents: str):
        self.contents = contents

    @abstractmethod
    def next_lasers(self, laser: Laser) -> list[Laser]:
        raise ValueError("Not supported", laser)


class DotCell(Cell):
    def __init__(self) -> None:
        self.contents = "."

    def next_lasers(self, laser: Laser) -> list[Laser]:
        row, col = laser.direction.offset(laser.row, laser.col)
        return [Laser(row, col, laser.direction)]


class DashCell(Cell):
    def __init__(self) -> None:
        self.contents = "-"

    def next_lasers(self, laser: Laser) -> list[Laser]:
        if laser.direction in [Direction.EAST, Direction.WEST]:
            row, col = laser.direction.offset(laser.row, laser.col)
            return [Laser(row, col, laser.direction)]
        row, col = laser.row, laser.col
        return [
            Laser(row, col + 1, Direction.EAST),
            Laser(row, col - 1, Direction.WEST),
        ]


class PipeCell(Cell):
    def __init__(self) -> None:
        self.contents = "|"

    def next_lasers(self, laser: Laser) -> list[Laser]:
        if laser.direction in [Direction.NORTH, Direction.SOUTH]:
            row, col = laser.direction.offset(laser.row, laser.col)
            return [Laser(row, col, laser.direction)]
        row, col = laser.row, laser.col
        return [
            Laser(row - 1, col, Direction.NORTH),
            Laser(row + 1, col, Direction.SOUTH),
        ]


class ForwardSlashCell(Cell):
    def __init__(self) -> None:
        self.contents = "/"

    def next_lasers(self, laser: Laser) -> list[Laser]:
        row, col = laser.row, laser.col
        if laser.direction == Direction.EAST:
            return [Laser(row - 1, col, Direction.NORTH)]
        if laser.direction == Direction.NORTH:
            return [Laser(row, col + 1, Direction.EAST)]
        if laser.direction == Direction.SOUTH:
            return [Laser(row, col - 1, Direction.WEST)]
        if laser.direction == Direction.WEST:
            return [Laser(row + 1, col, Direction.SOUTH)]


class BackSlashCell(Cell):
    def __init__(self) -> None:
        self.contents = "\\"

    def next_lasers(self, laser: Laser) -> list[Laser]:
        row, col = laser.row, laser.col
        if laser.direction == Direction.EAST:
            return [Laser(row + 1, col, Direction.SOUTH)]
        if laser.direction == Direction.SOUTH:
            return [Laser(row, col + 1, Direction.EAST)]
        if laser.direction == Direction.NORTH:
            return [Laser(row, col - 1, Direction.WEST)]
        if laser.direction == Direction.WEST:
            return [Laser(row - 1, col, Direction.NORTH)]
