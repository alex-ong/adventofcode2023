"""day10"""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


PIPE_FONT = {
    "|": ["│", "║", "|"],
    "-": ["─", "═", "-"],
    "L": ["└", "╚", "L"],
    "J": ["┘", "╝", "J"],
    "7": ["┐", "╗", "7"],
    "F": ["┌", "╔", "F"],
    ".": [".", ".", "."],
    "S": ["S", "S", "S"],  # S is an "L" piece. manually done forehead
}


FONT = 2


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

    def opposite(self):
        if self == Direction.NORTH:
            return Direction.SOUTH
        if self == Direction.SOUTH:
            return Direction.NORTH
        if self == Direction.EAST:
            return Direction.WEST
        if self == Direction.WEST:
            return Direction.EAST
        raise RuntimeError("invalid direction")


@dataclass
class Pipe:
    row: int
    col: int
    character: str

    is_start: bool = False
    font: int = FONT
    is_loop: bool = False

    PIPE_DIRECTION: ClassVar[dict[str, list[Direction]]] = {
        "|": [Direction.NORTH, Direction.SOUTH],
        "-": [Direction.WEST, Direction.EAST],
        "L": [Direction.NORTH, Direction.EAST],
        "J": [Direction.NORTH, Direction.WEST],
        "7": [Direction.WEST, Direction.SOUTH],
        "F": [Direction.SOUTH, Direction.EAST],
    }

    def __post_init__(self):
        if self.character == "S":
            self.is_start = True

    def __str__(self):
        if self.is_start:
            return "S"
        if self.is_loop:
            return PIPE_FONT[self.character][FONT]
        return " "

    def next_direction(self, prev_direction: Direction | None = None):
        """Determine next direction based on where we came from"""
        mapping = self.PIPE_DIRECTION[self.character]
        if prev_direction == mapping[0]:
            return mapping[1]
        return mapping[0]

    def next_position(self, prev_direction: Direction | None):
        """
        calculate the next position. Return
        where we came from if we move to next tile, and the new position
        """
        next_direction = self.next_direction(prev_direction)
        return next_direction.opposite(), self.position.next_position(next_direction)

    @property
    def position(self):
        return Position(self.row, self.col)

    def __hash__(self):
        return hash(f"{self.row},{self.col}")


@dataclass
class Position:
    row: int
    col: int

    def next_position(self, direction: Direction):
        """Determine next position based on direction"""
        if direction == Direction.EAST:
            return Position(self.row, self.col + 1)
        elif direction == Direction.NORTH:
            return Position(self.row - 1, self.col)
        elif direction == Direction.WEST:
            return Position(self.row, self.col - 1)
        # direction == Direction.SOUTH
        return Position(self.row + 1, self.col)


@dataclass
class PipeMap:
    pipes: list[list[Pipe]]

    def get_pipe(self, position: Position) -> Pipe:
        """returns a pipe given its position"""
        return self.pipes[position.row][position.col]

    def __str__(self):
        return "\n".join("".join(str(pipe) for pipe in line) for line in self.pipes)


def process_input_line(row: int, line: str) -> list[Pipe]:
    """process a single line of input"""
    return [Pipe(row, col, char) for col, char in enumerate(line.strip())]


def read_input():
    """read the map"""
    with open("input.txt", "r", encoding="utf8") as file:
        pipes = [process_input_line(row, line) for row, line in enumerate(file)]
        pipe_map = PipeMap(pipes)
    return pipe_map


def find_s(pipe_map: PipeMap) -> Position:
    for row_idx, row in enumerate(pipe_map.pipes):
        finder = (col_idx for col_idx, pipe in enumerate(row) if pipe.is_start)
        try:
            col_idx = next(finder)
            return Position(row_idx, col_idx)
        except StopIteration:
            continue
    raise RuntimeError("No S pipe found!")


def calculate_s(start: Position, pipe_map: PipeMap):
    """Guaranteed that there will be two pipes going into us"""
    connecting = []
    directions = list(Direction)

    for direction in directions:
        pos: Position = start.next_position(direction)
        tile: Pipe = pipe_map.get_pipe(pos)
        opposite_direction = direction.opposite()
        if opposite_direction in Pipe.PIPE_DIRECTION[tile.character]:
            connecting.append(direction)

    # should now have connecting == [NORTH, EAST]:
    for character, directions in Pipe.PIPE_DIRECTION.items():
        if connecting[0] in directions and connecting[1] in directions:
            return character
    return None


def find_cycles(pipe_map: PipeMap):
    # first find S, and re-assign it
    s_position: Position = find_s(pipe_map)
    s_char: str = calculate_s(s_position, pipe_map)
    s_pipe: Pipe = pipe_map.get_pipe(s_position)
    s_pipe.character = s_char

    pipe_path: list[Pipe] = []
    current_pipe: Pipe = s_pipe
    direction: Direction | None = None
    while current_pipe != s_pipe or len(pipe_path) == 0:
        pipe_path.append(current_pipe)
        direction, position = current_pipe.next_position(direction)
        current_pipe = pipe_map.get_pipe(position)
        current_pipe.is_loop = True

    return pipe_path


def main():
    pipe_map = read_input()
    # q1
    pipe_path = find_cycles(pipe_map)
    print(len(pipe_path) / 2)
    print(pipe_map)

    # q2. Flood fill the outside, then subtract length of loop.
    # this one is easy because there is only one contiguous outside region


if __name__ == "__main__":
    main()
