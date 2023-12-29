"""day16 solution
"""


import os

from tqdm.contrib.concurrent import process_map

from day16.lib.direction import Direction
from day16.lib.laser import Laser
from day16.lib.parsers import get_input
from day16.lib.world import World

INPUT = "day16/input.txt"
INPUT_SMALL = "day16/input-small.txt"


def solve_task(task: Laser, world: World) -> int:
    """Calculates number of energized tiles"""
    return world.solve(task).num_energized()


def solve_task_wrapper(args: tuple[Laser, World]) -> int:
    """Wraps solve_task in multiprocessing, since it only takes one arg"""
    task, world = args
    return solve_task(task, world)


def part1(world: World) -> int:
    laser = Laser(0, 0, Direction.EAST)
    solved_world = world.solve(laser)
    return solved_world.num_energized()


def part2(world: World) -> int:
    tasks = []
    # part 2: brute force coz our impl is already cached/backtracked
    # 1T -> 3.3s
    # 12T -> 1.1s
    for col in range(world.num_cols):
        tasks.append((Laser(0, col, Direction.SOUTH), world))
        tasks.append((Laser(world.num_rows - 1, col, Direction.NORTH), world))

    for row in range(world.num_rows):
        tasks.append((Laser(row, 0, Direction.EAST), world))
        tasks.append((Laser(row, world.num_cols - 1, Direction.WEST), world))

    cpu_count = os.cpu_count() or 1
    chunk_size = (len(tasks) // cpu_count) + 1
    results: list[int]
    results = process_map(solve_task_wrapper, tasks, chunksize=chunk_size)  # type: ignore

    return max(results)


def main() -> None:
    """Main function"""
    world = get_input(INPUT)

    print(part1(world))
    print(part2(world))


if __name__ == "__main__":
    main()
