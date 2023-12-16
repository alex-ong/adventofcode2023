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

    score: int | None = None

    def rotate_world_cw(self) -> "World":
        rotated = list(zip(*self.data[::-1]))
        return World(rotated, self.left_is.rotate_cw())

    def rotate_world_ccw(self) -> "World":
        rotated = list(zip(*self.data))[::-1]
        return World(rotated, self.left_is.rotate_ccw())

    def __hash__(self):
        return hash(str(self.data) + ":" + str(self.left_is))

    def print_map(self):
        """prints the map nicely"""
        print("\n".join(str(row) for row in self.data))

    def print_correct(self):
        """Pirnt with north facing up"""
        world = self.correct_side()
        world.print_map()
        print(f"last action:{self.left_is}")

    def get_score(self):
        world = self.correct_side()
        return naive_score(world.data)

    def correct_side(self) -> "World":
        world = self
        if world.left_is == Direction.West:
            return self
        elif world.left_is == Direction.North:
            return world.rotate_world_cw()
        elif world.left_is == Direction.East:
            world = world.rotate_world_cw()
            world = world.rotate_world_cw()
            return world
        elif world.left_is == Direction.South:
            return world.rotate_world_ccw()
        raise ValueError(f"Unsupported Direction: {world.left_is}")


def naive_score(world_rows):
    """returns score assuming west is pointing left"""
    num_rows = len(world_rows)
    score = 0
    for index, row in enumerate(world_rows):
        o_count = row.count("O")
        score += o_count * (num_rows - index)
    return score


def simulate_row(row):
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


def simulate_world(world_rows):
    """simulates world by rolling to the left."""
    result = []
    for world_row in world_rows:
        result.append(simulate_row(world_row)[0])
    return result


def get_input():
    """grabs input, rotated so that left is north"""
    with open("input.txt") as file:
        world = list(file)

    return World(world)


def question2(world: World):
    cache: dict[World, int] = {}
    cycle_results: list[World] = []
    for cycle in range(10000):
        # left_is: north
        world = world.rotate_world_cw()
        world.data = simulate_world(world.data)

        # left is: west
        world = world.rotate_world_cw()
        world.data = simulate_world(world.data)

        # left is: south
        world = world.rotate_world_cw()
        world.data = simulate_world(world.data)
        world.score = world.get_score()
        # world.print_correct()
        print(cycle, world.score)
        # east here
        if world in cache:
            cycle_start = cache[world]
            cycle_end = cycle
            break
        cache[world] = cycle
        cycle_results.append(world)

        # left is east
        world = world.rotate_world_cw()
        world.data = simulate_world(world.data)

    cycle_length = cycle_end - cycle_start
    print(f"cycle length: {cycle_length}")

    final_target = 1000000000
    target = (final_target - cycle_start - 1) % cycle_length
    result = cycle_results[cycle_start + target]
    return result.score


def main():
    world = get_input()
    world = world.rotate_world_ccw()

    # world is rotated 90 degrees,
    # so we just need to sum rows instead of cols
    # q1:
    print(sum(simulate_row(row)[1] for row in world.data))

    world.data = simulate_world(world.data)
    print(question2(world))


if __name__ == "__main__":
    main()
