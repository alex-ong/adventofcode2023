"""day18 solution"""

from dataclasses import dataclass
from enum import StrEnum
from queue import Queue

from tile import EdgeTile, HoleTile, Tile


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

    wall_tiles = 0
    dug_tiles = 0

    def __init__(self, num_rows: int, num_cols: int) -> None:
        self.contents = [[Tile() for col in range(num_cols)] for row in range(num_rows)]
        self.num_rows = num_rows
        self.num_cols = num_cols

    def process_command(self, miner_pos: Position, command: Command) -> Position:
        """Process command, returning miner's new position"""
        offsets = generate_offsets(miner_pos, command.direction, command.steps)
        self.wall_tiles += len(offsets)
        for offset in offsets:
            self.contents[offset.row][offset.col] = EdgeTile(color=command.color)
        return offsets[-1]

    def dig_out(self) -> None:
        # digs out the non-perimeter tiles, returning how many were "dug out"

        # cache for what's been visited
        visited: list[list[bool]] = [
            [False for _ in range(self.num_cols)] for _ in range(self.num_rows)
        ]

        # list of nodes to explore
        to_process: Queue[Position] = Queue()
        to_process.put(Position(1, 1))

        while not to_process.empty():
            position: Position = to_process.get()
            if self.is_oob(position):
                continue
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
        """True if position out of bounds"""
        return (
            position.row < 0
            or position.row >= self.num_rows
            or position.col < 0
            or position.col >= self.num_cols
        )

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
    matrix.dig_out()
    print(matrix)
    print(f"Dug: {matrix.dug_tiles}")
    print(f"Wall: {matrix.wall_tiles}")
    print(f"Total: {matrix.dug_tiles + matrix.wall_tiles}")


if __name__ == "__main__":
    main()
