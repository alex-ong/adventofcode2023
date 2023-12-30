"""day17 solution."""
from typing import Optional

from colorama import Back

from day17.lib.classes import Step, WorldPart1, WorldPart2
from day17.lib.parsers import get_input

INPUT = "day17/input.txt"
INPUT_SMALL = "day17/input-small.txt"
INPUT_PT2 = "day17/input-pt2.txt"


def solve_and_print(world: WorldPart1) -> int:
    """Solve and print."""
    result = world.solve()
    world_string = [[str(val) for val in row] for row in world.costs]

    step: Optional[Step] = result
    while step is not None:
        output_str = Back.GREEN + str(step.direction) + Back.BLACK
        world_string[step.row][step.col] = output_str
        step = step.src_step

    print("\n".join("".join(val for val in row) for row in world_string))
    return result.total_cost


def part1(input: list[list[int]]) -> int:
    """Load input and solve part1.

    (minimum path, max 3 in one direction)
    """
    world: WorldPart1 = WorldPart1(input)
    return solve_and_print(world)


def part2(input: list[list[int]]) -> int:
    """Load input and solve part2.

    (minimum path, min 4, max 10 in one direction)
    """
    world: WorldPart2 = WorldPart2(input)
    return solve_and_print(world)


def main() -> None:
    """Load input and run part1/part2."""
    input: list[list[int]] = get_input(INPUT)
    # q1
    print(f"num steps: {part1(input)}")
    # q2
    print(f"num steps: {part2(input)}")


if __name__ == "__main__":
    main()
