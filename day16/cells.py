"""
Cell classes
"""
from abc import ABC, abstractmethod
from direction import Direction
from laser import LaserInstance


class Cell(ABC):
    @staticmethod
    def construct(contents):
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

    def __init__(self, contents):
        self.contents = contents

    @abstractmethod
    def next_lasers(self, laser: LaserInstance) -> list[LaserInstance]:
        raise ValueError("Not supported", laser)


class DotCell(Cell):
    def __init__(self):
        self.contents = "."

    def next_lasers(self, laser: LaserInstance) -> list[LaserInstance]:
        row, col = laser.direction.offset(laser.row, laser.col)
        return [LaserInstance(row, col, laser.direction)]


class DashCell(Cell):
    def __init__(self):
        self.contents = "-"

    def next_lasers(self, laser: LaserInstance) -> list[LaserInstance]:
        if laser.direction in [Direction.EAST, Direction.WEST]:
            row, col = laser.direction.offset(laser.row, laser.col)
            return [LaserInstance(row, col, laser.direction)]
        row, col = laser.row, laser.col
        return [
            LaserInstance(row, col + 1, Direction.EAST),
            LaserInstance(row, col - 1, Direction.WEST),
        ]


class PipeCell(Cell):
    def __init__(self):
        self.contents = "|"

    def next_lasers(self, laser: LaserInstance) -> list[LaserInstance]:
        if laser.direction in [Direction.NORTH, Direction.SOUTH]:
            row, col = laser.direction.offset(laser.row, laser.col)
            return [LaserInstance(row, col, laser.direction)]
        row, col = laser.row, laser.col
        return [
            LaserInstance(row - 1, col, Direction.NORTH),
            LaserInstance(row + 1, col, Direction.SOUTH),
        ]


class ForwardSlashCell(Cell):
    def __init__(self):
        self.contents = "/"

    def next_lasers(self, laser: LaserInstance) -> list[LaserInstance]:
        row, col = laser.row, laser.col
        if laser.direction == Direction.EAST:
            return [LaserInstance(row - 1, col, Direction.NORTH)]
        if laser.direction == Direction.NORTH:
            return [LaserInstance(row, col + 1, Direction.EAST)]
        if laser.direction == Direction.SOUTH:
            return [LaserInstance(row, col - 1, Direction.WEST)]
        if laser.direction == Direction.WEST:
            return [LaserInstance(row + 1, col, Direction.SOUTH)]


class BackSlashCell(Cell):
    def __init__(self):
        self.contents = "\\"

    def next_lasers(self, laser: LaserInstance) -> list[LaserInstance]:
        row, col = laser.row, laser.col
        if laser.direction == Direction.EAST:
            return [LaserInstance(row + 1, col, Direction.SOUTH)]
        if laser.direction == Direction.SOUTH:
            return [LaserInstance(row, col + 1, Direction.EAST)]
        if laser.direction == Direction.NORTH:
            return [LaserInstance(row, col - 1, Direction.WEST)]
        if laser.direction == Direction.WEST:
            return [LaserInstance(row - 1, col, Direction.NORTH)]
