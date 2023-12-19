"""day18 solution"""

from dataclasses import dataclass
from enum import StrEnum


@dataclass
class Position:
    row: int = 0
    col: int = 0


class Direction(StrEnum):
    Up = "U"
    Down = "D"
    Left = "L"
    Right = "R"

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.name


@dataclass
class Tile:
    contents: str = "."

    def __str__(self) -> str:
        return "."


@dataclass(kw_only=True)
class EdgeTile(Tile):
    contents: str = "#"
    color: str

    # 38 -> 48 for background
    TEXT_WHITE = "\033[38;2;255;255;255m"

    def text_color(self, r: int, g: int, b: int) -> str:
        return f"\033[38;2;{r};{g};{b}m"

    def __str__(self) -> str:
        r, g, b = [int(self.color[i * 2 : i * 2 + 2], 16) for i in range(3)]

        return f"{self.text_color(r,g,b)}{self.contents}{self.TEXT_WHITE}"


@dataclass
class Command:
    direction: Direction
    steps: int
    color: str


def generate_offsets(
    position: Position, direction: Direction, steps: int
) -> list[Position]:
    if direction == Direction.Right:
        return [Position(position.row, position.col + i) for i in range(1, steps + 1)]
    if direction == Direction.Left:
        return [Position(position.row, position.col - i) for i in range(1, steps + 1)]
    if direction == Direction.Down:
        return [Position(position.row + i, position.col) for i in range(1, steps + 1)]
    if direction == Direction.Up:
        return [Position(position.row - i, position.col) for i in range(1, steps + 1)]
    raise ValueError(f"Direction not supported{direction}")


class Matrix:
    contents: list[list[Tile]]
    num_rows: int
    num_cols: int

    def __init__(self, num_rows: int, num_cols: int) -> None:
        self.contents = [[Tile() for col in range(num_cols)] for row in range(num_rows)]
        self.num_rows = num_rows
        self.num_cols = num_cols

    def process_command(self, miner_pos: Position, command: Command) -> Position:
        """Process command, returning miner's new position"""
        offsets = generate_offsets(miner_pos, command.direction, command.steps)

        for offset in offsets:
            self.contents[offset.row][offset.col] = EdgeTile(color=command.color)
        return offsets[-1]

    def __str__(self) -> str:
        return "\n".join("".join(str(tile) for tile in row) for row in self.contents)


def get_dimensions(commands: list[Command]) -> Position:
    position = Position()
    max_row, max_col = 0, 0
    for command in commands:
        position = generate_offsets(position, command.direction, command.steps)[-1]
        max_row = max(position.row, max_row)
        max_col = max(position.col, max_col)
    return Position(max_row, max_col)


def get_input() -> list[Command]:
    commands = []
    with open("input-small.txt", encoding="utf-8") as file:
        for line in file:
            direction, steps, color = line.strip().split()
            instruction = Command(Direction(direction), int(steps), color[2:-1])
            commands.append(instruction)
    return commands


def main() -> None:
    commands: list[Command] = get_input()

    dimensions: Position = get_dimensions(commands)
    matrix: Matrix = Matrix(dimensions.row + 1, dimensions.col + 1)
    position = Position()
    for command in commands:
        position = matrix.process_command(position, command)

    print(matrix)


if __name__ == "__main__":
    main()
