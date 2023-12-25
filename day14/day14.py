"""day14 solution"""

from dataclasses import dataclass
from typing import Any

from day14.lib.direction import Direction

INPUT_SMALL = "day14/input-small.txt"
INPUT = "day14/input.txt"


@dataclass
class World:
    data: Any
    left_is: Direction = Direction.West

    score: int | None = None

    def rotate_world_cw(self) -> "World":
        rotated = list(zip(*self.data[::-1]))
        return World(rotated, self.left_is.next_direction_ccw())

    def rotate_world_ccw(self) -> "World":
        rotated = list(zip(*self.data))[::-1]
        return World(rotated, self.left_is.next_direction_cw())

    def __hash__(self) -> int:
        return hash(str(self.data) + ":" + str(self.left_is))

    def to_string(self) -> str:
        return "\n".join(str(row) for row in self.data)

    def print_map(self) -> None:
        """prints the map nicely"""
        print(self.to_string())

    def print_correct(self) -> None:
        """Print with north facing up"""
        world = self.correct_side()
        world.print_map()
        print(f"last action:{self.left_is}")

    def get_score(self) -> int:
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


def naive_score(world_rows: list[str]) -> int:
    """returns score assuming west is pointing left"""
    num_rows = len(world_rows)
    score = 0
    for index, row in enumerate(world_rows):
        o_count = row.count("O")
        score += o_count * (num_rows - index)
    return score


def simulate_row(row: list[str]) -> tuple[list[str], int]:
    """
    simulates a row; returns its value and the new row
    Assume's that we are moving boulders to the left
    """
    square_indices = [-1] + [i for i, x in enumerate(row) if x == "#"] + [len(row)]
    pairs = zip(square_indices, square_indices[1:])
    row_score = 0
    new_row = ""
    for start, end in pairs:
        sub_array = row[start + 1 : end]
        o_count = sub_array.count("O")
        start_score = len(row) - (start + 1)
        end_score = len(row) - start - o_count
        sub_array_score = int((start_score + end_score) / 2 * o_count)
        row_score += sub_array_score
        new_row += "O" * o_count
        new_row += "." * (end - start - o_count - 1)
        new_row += "#"

    new_row = new_row[:-1]
    return list(new_row), row_score


def simulate_world(world_rows: list[list[str]]) -> list[list[str]]:
    """simulates world by rolling to the left."""
    result = []
    for world_row in world_rows:
        result.append(simulate_row(world_row)[0])
    return result


def get_input(path: str) -> World:
    """grabs input, rotated so that left is north"""
    with open(path) as file:
        lines = [line.strip() for line in file]

    return World(lines)


def question1(world: World) -> int:
    while world.left_is != Direction.North:
        world = world.rotate_world_ccw()
    return sum(simulate_row(row)[1] for row in world.data)


def question2(world: World) -> int:
    cache: dict[World, int] = {}
    cycle_results: list[World] = []

    # starting state: left_is north
    while world.left_is != Direction.North:
        world = world.rotate_world_ccw()
    world.data = simulate_world(world.data)

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

    if result.score is None:
        raise ValueError("No score found!")
    return result.score


def main() -> None:
    world = get_input(INPUT)

    print(question1(world))
    print(question2(world))


if __name__ == "__main__":
    main()
