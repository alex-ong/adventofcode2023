from dataclasses import dataclass, field
from typing import ClassVar

from day10.lib.direction import Direction
from day10.lib.pipebounds import PipeBounds
from day10.lib.position import Position

PIPE_FONT = {
    "|": ["│", "║", "|", "X"],
    "-": ["─", "═", "-", "X"],
    "L": ["└", "╚", "L", "X"],
    "J": ["┘", "╝", "J", "X"],
    "7": ["┐", "╗", "7", "X"],
    "F": ["┌", "╔", "F", "X"],
    ".": [".", ".", ".", "X"],
    "S": ["S", "S", "S", "S"],  # S is an "L" piece. manually done forehead
}


FONT = 1


@dataclass
class Pipe:
    row: int
    col: int
    character: str

    is_start: bool = field(init=False)
    font: int = FONT
    is_loop: bool = False
    pipe_bounds: PipeBounds = PipeBounds.UNKNOWN

    PIPE_DIRECTION: ClassVar[dict[str, list[Direction]]] = {
        "|": [Direction.NORTH, Direction.SOUTH],
        "-": [Direction.WEST, Direction.EAST],
        "L": [Direction.NORTH, Direction.EAST],
        "J": [Direction.NORTH, Direction.WEST],
        "7": [Direction.WEST, Direction.SOUTH],
        "F": [Direction.SOUTH, Direction.EAST],
        ".": [],
    }

    def __post_init__(self) -> None:
        self.is_start = self.character == "S"
        if self.is_loop:
            self.pipe_bounds = PipeBounds.PIPE

    def __str__(self) -> str:
        if self.is_start:
            return "S"
        if self.is_loop:
            return PIPE_FONT[self.character][FONT]
        if self.pipe_bounds == PipeBounds.INSIDE:
            return "*"
        if self.pipe_bounds == PipeBounds.OUTSIDE:
            return "."
        return " "

    def next_direction(self, prev_direction: Direction | None = None) -> Direction:
        """Determine next direction based on where we came from"""
        mapping = self.PIPE_DIRECTION[self.character]
        if prev_direction == mapping[0]:
            return mapping[1]
        return mapping[0]

    def next_position(
        self, prev_direction: Direction | None
    ) -> tuple[Direction, Position]:
        """
        calculate the next position. Return
        where we came from if we move to next tile, and the new position
        """
        next_direction = self.next_direction(prev_direction)
        return next_direction.opposite(), self.position.next_position(next_direction)

    @property
    def position(self) -> Position:
        return Position(self.row, self.col)

    def __hash__(self) -> int:  # pragma: no cover
        return hash(f"{self.row},{self.col}")


@dataclass
class PipeMap:
    pipes: list[list[Pipe]]

    width: int = field(init=False, repr=False)
    height: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.width = len(self.pipes[0])
        self.height = len(self.pipes)

    def get_pipe(self, position: Position) -> Pipe:
        """returns a pipe given its position"""
        if not self.is_in_map(position):
            raise ValueError(f"Position outside map {position}")
        return self.pipes[position.row][position.col]

    def is_in_map(self, position: Position) -> bool:
        return 0 <= position.row < self.height and 0 <= position.col < self.width

    def get_pipe_safe(self, position: Position) -> Pipe | None:
        if self.is_in_map(position):
            return self.pipes[position.row][position.col]
        return None

    def __str__(self) -> str:
        return "\n".join("".join(str(pipe) for pipe in line) for line in self.pipes)
