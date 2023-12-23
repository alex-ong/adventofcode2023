from dataclasses import dataclass

from day10.lib.direction import Direction


@dataclass
class Position:
    row: int
    col: int

    def next_position(self, direction: Direction) -> "Position":
        """Determine next position based on direction"""
        if direction == Direction.EAST:
            return Position(self.row, self.col + 1)
        elif direction == Direction.NORTH:
            return Position(self.row - 1, self.col)
        elif direction == Direction.WEST:
            return Position(self.row, self.col - 1)
        elif direction == Direction.SOUTH:
            return Position(self.row + 1, self.col)
        elif direction == Direction.NORTH_EAST:
            return Position(self.row - 1, self.col + 1)
        elif direction == Direction.NORTH_WEST:
            return Position(self.row - 1, self.col - 1)
        elif direction == Direction.SOUTH_WEST:
            return Position(self.row + 1, self.col - 1)
        elif direction == Direction.SOUTH_EAST:
            return Position(self.row + 1, self.col + 1)
        raise ValueError(f"invalid direction {direction}")

    def __hash__(self) -> int:
        return hash(f"{self.row}:{self.col}")
