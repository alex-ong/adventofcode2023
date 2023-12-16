"""day14 solution"""

from dataclasses import dataclass
from enum import IntEnum, Enum
from typing import Any


class Direction(IntEnum):
    North = 0
    West = 1
    South = 2
    East = 3

    __str__ = Enum.__str__

    def rotate_ccw(self):
        int_value = int(self)
        return Direction((int_value - 1 + len(Direction)) % len(Direction))

    def rotate_cw(self):
        int_value = int(self)
        return Direction((int_value + 1) % len(Direction))


@dataclass
class World:
    data: Any
    left_is: Direction = Direction.West

    def rotate_world_cw(self) -> "World":
        rotated = list(zip(*self.data[::-1]))
        return World(rotated, self.left_is.rotate_cw())

    def rotate_world_ccw(self) -> "World":
        rotated = list(zip(*self.data))[::-1]
        return World(rotated, self.left_is.rotate_ccw())

    def __hash__(self):
        return hash(str(self.data) + ":" + str(self.left_is))

    def print_map(self):
        print("\n".join(str(row) for row in self.data))
        print(self.left_is)


def simulate_row(row) -> tuple[list[str], int]:
    """simulates a row; returns its value and the new row"""
    square_indices = [-1] + [i for i, x in enumerate(row) if x == "#"] + [len(row)]
    pairs = zip(square_indices, square_indices[1:])
    row_score = 0
    new_row = ""
    for start, end in pairs:
        sub_array = row[start + 1 : end]
        o_count = sub_array.count("O")
        start_score = len(row) - (start + 1)
        end_score = len(row) - start - o_count
        sub_array_score = (start_score + end_score) / 2 * o_count
        row_score += sub_array_score
        new_row += "O" * o_count
        new_row += "." * (end - start - o_count - 1)
        new_row += "#"

    new_row = new_row[:-1]
    return list(new_row), row_score


def get_input():
    """grabs input, rotated so that left is north"""
    with open("input-arrow.txt") as file:
        world = list(file)

    return World(world)


def main():
    world = get_input()
    world = world.rotate_world_ccw()

    # world is rotated 90 degrees,
    # so we just need to sum rows instead of cols
    # q1:
    print(sum(simulate_row(row)[1] for row in world.data))

    # q2:
    world.print_map()
    world = world.rotate_world_cw()
    world.print_map()
    world = world.rotate_world_cw()
    world.print_map()
    world = world.rotate_world_cw()
    world.print_map()


if __name__ == "__main__":
    main()
