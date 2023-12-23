"""laser instance class"""
from dataclasses import dataclass

from day16.lib.direction import Direction


@dataclass
class Laser:
    row: int
    col: int

    direction: Direction

    def __hash__(self) -> int:
        return hash(str(self.row) + ":" + str(self.col) + "|" + str(self.direction))
