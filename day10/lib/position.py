"""Position class."""
from dataclasses import dataclass

from day10.lib.direction import Direction


@dataclass
class Position:
    """Simple 2d coordinate."""

    row: int
    col: int

    def next_position(self, direction: Direction) -> "Position":
        """Determine next position based on direction."""
        if direction == Direction.EAST:
            return Position(self.row, self.col + 1)
        elif direction == Direction.NORTH:
            return Position(self.row - 1, self.col)
        elif direction == Direction.WEST:
            return Position(self.row, self.col - 1)
        elif direction == Direction.SOUTH:
            return Position(self.row + 1, self.col)

        raise AssertionError(f"invalid direction {direction}")

    def __hash__(self) -> int:
        """Custom hash function so we can compare positions."""
        return hash(f"{self.row}:{self.col}")
