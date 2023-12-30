"""day18 solution."""

from dataclasses import dataclass
from enum import StrEnum
from queue import Queue

from day18.lib.tile import EdgeTile, HoleTile, Tile

INPUT = "day18/input.txt"
INPUT_SMALL = "day18/input-small.txt"


@dataclass
class Position:
    """Simple 2d point."""

    row: int = 0
    col: int = 0


class Direction(StrEnum):
    """Cardinal direction in ``UDLR``."""

    Up = "U"
    Down = "D"
    Left = "L"
    Right = "R"

    def __repr__(self) -> str:  # pragma: no cover
        """Custom repr for easy printing."""
        return str(self)

    def __str__(self) -> str:
        """Up/Down/Left/Right."""
        return self.name


@dataclass(frozen=True)
class Command:
    """Well defined command dataclass."""

    direction: Direction
    steps: int
    color: str


def generate_offsets(
    position: Position, direction: Direction, steps: int
) -> list[Position]:
    """Generate position offsets.

    Args:
        position (Position): base position
        direction (Direction): direction of travel
        steps (int): number of steps to generate

    Raises:
        AssertionError: If direciton is invalid.

    Returns:
        list[Position]: list of new positions.
    """
    if direction == Direction.Right:
        return [Position(position.row, position.col + i) for i in range(1, steps + 1)]
    if direction == Direction.Left:
        return [Position(position.row, position.col - i) for i in range(1, steps + 1)]
    if direction == Direction.Down:
        return [Position(position.row + i, position.col) for i in range(1, steps + 1)]
    if direction == Direction.Up:
        return [Position(position.row - i, position.col) for i in range(1, steps + 1)]
    raise AssertionError(f"Direction not supported{direction}")


class Matrix:
    """2d array representing world."""

    contents: list[list[Tile]]

    min_pos: Position
    max_pos: Position

    num_rows: int
    num_cols: int

    wall_tiles = 0
    dug_tiles = 0

    def __init__(self, min_pos: Position, max_pos: Position) -> None:
        """Generate 2d array with min/max position for offsetting."""
        self.num_rows = max_pos.row - min_pos.row + 1
        self.num_cols = max_pos.col - min_pos.col + 1
        self.contents = [
            [Tile() for _ in range(self.num_cols)] for _ in range(self.num_rows)
        ]

    def process_command(self, miner_pos: Position, command: Command) -> Position:
        """Process command.

        This moves the miner around.

        Args:
            miner_pos (Position): miner's current position
            command (Command): command to process

        Returns:
            Position: miner's new position.
        """
        offsets = generate_offsets(miner_pos, command.direction, command.steps)
        self.wall_tiles += len(offsets)
        for offset in offsets:
            self.contents[offset.row][offset.col] = EdgeTile(color=command.color)
        return offsets[-1]

    def dig_out(self) -> None:
        """Dig out non-perimeter tiles using flood-fill."""
        # cache for what's been visited
        visited: list[list[bool]] = [
            [False for _ in range(self.num_cols)] for _ in range(self.num_rows)
        ]

        # list of nodes to explore
        to_process: Queue[Position] = Queue()
        to_process.put(Position(self.num_rows // 2, self.num_cols // 2))

        while not to_process.empty():
            position: Position = to_process.get()
            if self.is_oob(position):
                raise AssertionError("pre-allocated matrix shouldn't cause OOB")
            if visited[position.row][position.col]:
                continue
            if self.contents[position.row][position.col].contents != ".":
                continue
            self.contents[position.row][position.col] = HoleTile()
            visited[position.row][position.col] = True
            self.dug_tiles += 1

            for direction in Direction:
                to_process.put(generate_offsets(position, direction, 1)[0])

    def is_oob(self, position: Position) -> bool:
        """Returns if a position is out of bounds.

        Args:
            position (Position): position to check.

        Returns:
            bool: True if out of bounds.
        """
        return (
            position.row < 0
            or position.row >= self.num_rows
            or position.col < 0
            or position.col >= self.num_cols
        )

    def __str__(self) -> str:
        """Custom __str__ for pretty printing matrix."""
        return "\n".join("".join(str(tile) for tile in row) for row in self.contents)


def get_matrix_range(commands: list[Command]) -> tuple[Position, Position]:
    """Calculate minimum and maximum position in matrix.

    Since we start in the middle somewhere, we get negative positions.
    This can be useds to offset the matrix when we construct it.

    Args:
        commands (list[Command]): list of commands that will be run.

    Returns:
        tuple[Position, Position]: [min,max] positions.
    """
    position = Position()
    max_row, max_col = 0, 0
    min_row, min_col = 0, 0
    for command in commands:
        position = generate_offsets(position, command.direction, command.steps)[-1]
        min_row = min(position.row, min_row)
        min_col = min(position.col, min_col)
        max_row = max(position.row, max_row)
        max_col = max(position.col, max_col)
    return Position(min_row, min_col), Position(max_row, max_col)


def get_input(path: str) -> list[Command]:
    """Reads input from file into well-formed list of commands."""
    commands = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            direction, steps, color = line.strip().split()
            instruction = Command(Direction(direction), int(steps), color[2:-1])
            commands.append(instruction)
    return commands


def get_solution(commands: list[Command]) -> int:
    """Calculates solution.

    1. Pre-calculates the range
    2. Creates edge tiles
    3. Flood fill centre.
    4. Count tiles.
    """
    min_pos, max_pos = get_matrix_range(commands)

    matrix: Matrix = Matrix(min_pos, max_pos)
    position: Position = Position(-min_pos.row, -min_pos.col)
    for command in commands:
        position = matrix.process_command(position, command)

    print(matrix)
    matrix.dig_out()
    print("\n" * 10)
    print(matrix)
    print(f"Dug: {matrix.dug_tiles}")
    print(f"Wall: {matrix.wall_tiles}")
    print(f"Total: {matrix.dug_tiles + matrix.wall_tiles}")
    return matrix.dug_tiles + matrix.wall_tiles


def main() -> None:
    """Load data and then find solution to part1."""
    commands: list[Command] = get_input(INPUT)
    get_solution(commands)


if __name__ == "__main__":
    main()
