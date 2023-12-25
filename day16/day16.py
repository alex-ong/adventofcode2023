"""
day16 solution
"""


from day16.lib.direction import Direction
from day16.lib.laser import Laser
from day16.lib.parsers import get_input
from day16.lib.world import World

INPUT = "day16/input.txt"
INPUT_SMALL = "day16/input-small.txt"


def solve_task(task: Laser, world: World) -> int:
    """Calculates number of energized tiles"""
    return world.solve(task).num_energized()


def part1(world: World) -> int:
    laser = Laser(0, 0, Direction.EAST)
    solved_world = world.solve(laser)
    return solved_world.num_energized()


def part2(world: World) -> int:
    tasks = []
    # part 2: brute force coz our impl is already cached/backtracked
    for col in range(world.num_cols):
        tasks.append(Laser(0, col, Direction.SOUTH))
        tasks.append(Laser(world.num_rows - 1, col, Direction.NORTH))

    for row in range(world.num_rows):
        tasks.append(Laser(row, 0, Direction.EAST))
        tasks.append(Laser(row, world.num_cols - 1, Direction.WEST))

    return max(solve_task(task, world) for task in tasks)


def main() -> None:
    """main function"""
    world = get_input(INPUT)

    print(part1(world))
    print(part2(world))


if __name__ == "__main__":
    main()
