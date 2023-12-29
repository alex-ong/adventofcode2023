"""day14 solution."""

from dataclasses import dataclass
from typing import Any, Optional

from day14.lib.direction import Direction

INPUT_SMALL = "day14/input-small.txt"
INPUT = "day14/input.txt"


@dataclass
class World:
    """2d array of boulders (square/round) and empty space."""

    data: Any
    left_is: Direction = Direction.West

    score: int | None = None

    def rotate_world_cw(self) -> "World":
        """Rotate world clockwise."""
        rotated = list(zip(*self.data[::-1]))
        return World(rotated, self.left_is.next_direction_ccw())

    def rotate_world_ccw(self) -> "World":
        """Rotate world anti-clockwise."""
        rotated = list(zip(*self.data))[::-1]
        return World(rotated, self.left_is.next_direction_cw())

    def __hash__(self) -> int:
        """Custom hash function for use with ``set()``."""
        return hash(str(self.data) + ":" + str(self.left_is))

    def to_string(self) -> str:
        """Well defined string of our world."""
        return "\n".join(str(row) for row in self.data)

    def as_orientiented_north(self) -> str:
        """Well defined string if our world has up as North."""
        world = self.correct_side()
        return world.to_string()

    def get_score(self) -> int:
        """Get score of the world."""
        world = self.correct_side()
        return naive_score(world.data)

    def correct_side(self) -> "World":
        """Return world oriented with North at the top."""
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
        raise AssertionError(f"Unsupported Direction: {world.left_is}")


def naive_score(world_rows: list[str]) -> int:
    """Returns score assuming west is pointing left.

    For each row, a round boulder ``O``'s score is
    ``num_rows`` minus its ``index``(higher weight to the left.)
    """
    num_rows = len(world_rows)
    score = 0
    for index, row in enumerate(world_rows):
        o_count = row.count("O")
        score += o_count * (num_rows - index)
    return score


def simulate_row(row: list[str]) -> tuple[list[str], int]:
    """Simulates a row; returns its value and the new row.

    Assumes that we are moving boulders to the left
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
    """Simulates world by rolling to the left."""
    result = []
    for world_row in world_rows:
        result.append(simulate_row(world_row)[0])
    return result


def get_input(path: str) -> World:
    """Grabs input, rotated so that left is north."""
    with open(path) as file:
        lines = [line.strip() for line in file]

    return World(lines)


def question1(world: World) -> int:
    """Returns world's score after rotating the world once."""
    while world.left_is != Direction.North:
        world = world.rotate_world_ccw()
    return sum(simulate_row(row)[1] for row in world.data)


def question2(world: World) -> int:
    """Finds a loop in world rotation.

    Once the loop is found we can estimate the world's state
    after any amount of rotations

    Args:
        world (World): world to spin

    Returns:
        int: "weight" to the north after 1000000000 cycles.
    """
    cache: dict[World, int] = {}
    cycle_results: list[World] = []

    # starting state: left_is north
    while world.left_is != Direction.North:
        world = world.rotate_world_ccw()
    world.data = simulate_world(world.data)

    cycle_index = 0
    cycle_start: Optional[int] = None
    cycle_end: Optional[int] = None

    while cycle_start is None and cycle_end is None:
        for direction in [
            Direction.North,  # left_is north
            Direction.West,  # left_is west
            Direction.South,  # left_is south
            Direction.East,  # left_is east
        ]:
            if direction == Direction.East:  # calculate score *before*
                if world in cache:
                    cycle_start = cache[world]
                    cycle_end = cycle_index
                else:
                    cache[world] = cycle_index
                    cycle_results.append(world)
            world = world.rotate_world_cw()
            world.data = simulate_world(world.data)
            world.score = world.get_score()

        cycle_index += 1

    if cycle_end is None or cycle_start is None:
        raise AssertionError("cycle_end and cycle_end should not be None")

    cycle_length = cycle_end - cycle_start
    print(f"cycle length: {cycle_length}")

    final_target = 1000000000
    target = (final_target - cycle_start - 1) % cycle_length
    result = cycle_results[cycle_start + target]

    if result.score is None:
        raise AssertionError("No score found!")

    return result.score


def main() -> None:
    """Get input and run question1/question2."""
    world = get_input(INPUT)

    print(question1(world))
    print(question2(world))


if __name__ == "__main__":
    main()
