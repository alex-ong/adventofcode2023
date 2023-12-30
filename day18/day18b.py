"""Day18b solution."""
from dataclasses import dataclass
from enum import IntEnum

INPUT = "day18/input.txt"
INPUT_SMALL = "day18/input-small.txt"


@dataclass
class Position:
    """Simple 2d vector."""

    row: int = 0
    col: int = 0


class Direction(IntEnum):
    """Direction as an integer enum."""

    Right = 0
    Down = 1
    Left = 2
    Up = 3


@dataclass(init=False)
class Command:
    """Command from hexstring."""

    direction: Direction
    steps: int

    def __init__(self, hexcode: str):
        """Converts from hexcode to well formed direction+steps."""
        self.steps = int(hexcode[:5], 16)
        self.direction = Direction(int(hexcode[-1]))


def get_input(path: str) -> list[Command]:
    """Grabs input from file, parsing into well-formed commands."""
    commands = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            hexcode = line.strip().split()[2]
            instruction = Command(hexcode[2:-1])
            commands.append(instruction)
    return commands


def process_command(command: Command, position: Position) -> Position:
    """Process a command and return new position."""
    if command.direction == Direction.Right:
        return Position(position.row, position.col + command.steps)
    if command.direction == Direction.Down:
        return Position(position.row + command.steps, position.col)
    if command.direction == Direction.Left:
        return Position(position.row, position.col - command.steps)
    if command.direction == Direction.Up:
        return Position(position.row - command.steps, position.col)
    raise AssertionError(f"unsupported directoin {command.direction}")


def calculate_area(positions: list[Position], perimeter: int) -> int:
    """Calculate area using shoelace area."""
    # total_area = shoelace_area + (perimeter_length // 2) + 1

    # shoelace assumes that each point is in centre, but each
    # perimeter tile is only "half" counted
    n = len(positions)  # of corners
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += positions[i].row * positions[j].col
        area -= positions[j].row * positions[i].col
    area = abs(area) // 2

    return area + (perimeter // 2) + 1


def get_solution(commands: list[Command]) -> int:
    """Get solution via processing commands then running shoelace area."""
    positions: list[Position] = []
    position = Position()

    for command in commands:
        position = process_command(command, position)
        positions.append(position)

    perimeter = sum(command.steps for command in commands)

    return calculate_area(positions, perimeter)


def main() -> None:
    """Grab input and then pass it into solver."""
    commands: list[Command] = get_input(INPUT)

    print(get_solution(commands))


if __name__ == "__main__":
    main()
