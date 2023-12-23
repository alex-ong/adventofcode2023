from dataclasses import dataclass
from enum import IntEnum


@dataclass
class Position:
    row: int = 0
    col: int = 0


class Direction(IntEnum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3


@dataclass(init=False)
class Command:
    direction: Direction
    steps: int

    def __init__(self, hexcode: str):
        self.steps = int(hexcode[:5], 16)
        self.direction = Direction(int(hexcode[-1]))


def get_input() -> list[Command]:
    commands = []
    with open("day18/input.txt", encoding="utf-8") as file:
        for line in file:
            hexcode = line.strip().split()[2]
            instruction = Command(hexcode[2:-1])
            commands.append(instruction)
    return commands


def process_command(command: Command, position: Position) -> Position:
    if command.direction == Direction.Right:
        return Position(position.row, position.col + command.steps)
    if command.direction == Direction.Down:
        return Position(position.row + command.steps, position.col)
    if command.direction == Direction.Left:
        return Position(position.row, position.col - command.steps)
    if command.direction == Direction.Up:
        return Position(position.row - command.steps, position.col)
    raise ValueError(f"unsupported directoin {command.direction}")


def calculate_area(positions: list[Position], perimeter: int) -> int:
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


def main() -> None:
    commands: list[Command] = get_input()

    positions: list[Position] = []
    position = Position()

    for command in commands:
        position = process_command(command, position)
        positions.append(position)

    perimeter = sum(command.steps for command in commands)

    print(calculate_area(positions, perimeter))


if __name__ == "__main__":
    main()
