"""laser instance class"""
from dataclasses import dataclass
from direction import Direction


@dataclass
class LaserInstance:
    row: int
    col: int

    direction: Direction

    def __hash__(self):
        return hash(str(self.row) + ":" + str(self.col) + "|" + str(self.direction))
