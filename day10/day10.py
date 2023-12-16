"""day10"""

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar


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


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4
    NORTH_EAST = 5
    NORTH_WEST = 6
    SOUTH_EAST = 7
    SOUTH_WEST = 8

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


class PipeBounds(Enum):
    INSIDE = 0
    OUTSIDE = 1
    UNKNOWN = 2
    PIPE = 3


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
    }

    def __post_init__(self):
        self.is_start = self.character == "S"
        if self.is_loop:
            self.pipe_bounds = PipeBounds.PIPE

    def __str__(self):
        if self.is_start:
            return "S"
        if self.is_loop:
            return PIPE_FONT[self.character][FONT]
        if self.pipe_bounds == PipeBounds.INSIDE:
            return "*"
        if self.pipe_bounds == PipeBounds.OUTSIDE:
            return "."
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

    def __hash__(self):
        return hash(f"{self.row}:{self.col}")


@dataclass
class PipeMap:
    pipes: list[list[Pipe]]

    @property
    def width(self):
        return len(self.pipes[0])

    @property
    def height(self):
        return len(self.pipes)

    def get_pipe(self, position: Position) -> Pipe:
        """returns a pipe given its position"""
        return self.pipes[position.row][position.col]

    def get_pipe_safe(self, position: Position) -> Pipe | None:
        if 0 <= position.row < self.height and 0 <= position.col < self.width:
            return self.get_pipe(position)
        return None

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
    """Finds the S pipe"""
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
    pipe_directions = [Direction.NORTH, Direction.WEST, Direction.EAST, Direction.SOUTH]

    for direction in pipe_directions:
        pos: Position = start.next_position(direction)
        tile: Pipe | None = pipe_map.get_pipe(pos)
        if tile is None:
            raise RuntimeError("Expecting valid pipe")
        opposite_direction = direction.opposite()
        if opposite_direction in Pipe.PIPE_DIRECTION[tile.character]:
            connecting.append(direction)

    # should now have connecting == [NORTH, EAST]:
    for character, pipe_directions in Pipe.PIPE_DIRECTION.items():
        if set(connecting) == set(pipe_directions):
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


def flood_fill(pipe_map: PipeMap):
    """
    flood fills a pipemap from one starting tile
    returns how many tiles were filled
    """
    visited_positions = set()
    to_visit: list[Position] = [Position(0, 0)]

    directions = list(Direction)
    num_outside = 0
    while len(to_visit) > 0:
        position = to_visit.pop()

        if position in visited_positions:
            continue

        # mark the position as outside
        pipe: Pipe | None = pipe_map.get_pipe(position)
        if pipe is not None and not pipe.is_loop:
            pipe.pipe_bounds = PipeBounds.OUTSIDE
            num_outside += 1
            for direction in directions:
                new_position = position.next_position(direction)
                to_visit.append(new_position)
        visited_positions.add(position)

    return num_outside


def process_big_input_line(row: int, line: str) -> list[Pipe]:
    """process a single line of input"""
    return [
        Pipe(row, col, char, is_loop=(char != " ")) for col, char in enumerate(line)
    ]


def expand_map(pipe_map: PipeMap):
    """expands each pipe into a 3x3 tile"""
    big_map = []

    for row in pipe_map.pipes:
        # three rows per original row:
        big_rows = ["", "", ""]

        for col in row:
            big_pipe = expand_pipe(col.character, col.is_loop)

            for row_idx, big_row in enumerate(big_pipe):
                big_rows[row_idx] += big_row

        big_map.extend(big_rows)

    # now convert big_map into "nice" pipes:
    pipes = [process_big_input_line(row, line) for row, line in enumerate(big_map)]

    pipe_map = PipeMap(pipes)
    return pipe_map


def reduce_map(big_map: PipeMap, small_map: PipeMap):
    """converts from fat map back down to small map"""
    rows = []
    for row_idx in range(small_map.height):
        row_tiles = []
        big_map_row_idx = row_idx * 3 + 1
        for col_idx in range(small_map.width):
            big_map_col_idx = col_idx * 3 + 1
            position = Position(big_map_row_idx, big_map_col_idx)
            tile = big_map.get_pipe(position)
            new_tile = Pipe(
                row_idx,
                col_idx,
                tile.character,
                is_loop=tile.is_loop,
                pipe_bounds=tile.pipe_bounds,
            )
            row_tiles.append(new_tile)
        rows.append(row_tiles)

    return PipeMap(rows)


def expand_pipe(character: str, is_loop: bool):
    # expands a pipe character to big boi 3x3
    # fmt: off
    if not is_loop:
        return ("   ",
                "   ",
                "   ")
        
    if character == "|":
        return (" | ",
                " | ",
                " | ")
    
    if character == "-":
        return ("   ", 
                "---", 
                "   ")
    
    if character == "L":
        return (" | ", 
                " L-", 
                "   ")
    if character == "J":
        return (" | ", 
                "-J ", 
                "   ")
    if character == "7":
        return ("   ", 
                "-7 ", 
                " | ")
    
    if character == "F":
        return ("   ", 
                " F-", 
                " | ")

    # fmt: on


def main():
    pipe_map = read_input()
    # q1
    pipe_path = find_cycles(pipe_map)
    print(len(pipe_path) / 2)
    print(pipe_map)

    # q2. Flood fill the outside, then subtract length of loop.
    # this one is easy because there is only one contiguous outside region
    # outside = flood_fill(pipe_map)

    big_map: PipeMap = expand_map(pipe_map)

    # you can use this to view it lol.
    with open("big_unfilled.txt", "w", encoding="utf8") as file:
        file.write(str(big_map))

    flood_fill(big_map)
    with open("big_filled.txt", "w", encoding="utf8") as file:
        file.write(str(big_map))

    small_map: PipeMap = reduce_map(big_map, pipe_map)
    pipes = small_map.pipes
    total_unknown = 0
    for row in pipes:
        total_unknown += sum(
            1 if col.pipe_bounds == PipeBounds.UNKNOWN else 0 for col in row
        )
    print(total_unknown)
    # extra: mark all the insides as inside:


if __name__ == "__main__":
    main()
