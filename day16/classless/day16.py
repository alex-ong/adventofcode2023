"""
day16 solution
"""


import time
from dataclasses import dataclass, field

import cell
from direction import EAST, NORTH, SOUTH, WEST


class SolvedWorld:
    data: list[list[list[tuple[int, int, int]]]]

    def __init__(self, num_rows: int, num_cols: int):
        self.data = [[[] for _ in range(num_cols)] for _ in range(num_rows)]

    def already_solved(self, row, col, direction) -> bool:
        """returns true if laser already calculated"""
        solutions = self.data[row][col]
        if (row, col, direction) in solutions:
            return True
        return False

    def add_laser(self, row, col, direction) -> None:
        """adds laser to cell"""
        solutions = self.data[row][col]
        solutions.append((row, col, direction))

    def __str__(self) -> str:
        row_strs = []
        for row in self.data:
            row_str = "".join(str(len(col)) for col in row)
            row_strs.append(row_str)
        return "\n".join(row_strs)

    def num_energized(self) -> int:
        """Return number of energized cells"""
        result: int = 0
        for row in self.data:
            result += sum(1 if len(col) >= 1 else 0 for col in row)
        return result


@dataclass
class World:
    data: list[list[str]]

    num_rows: int = field(init=False, repr=False)
    num_cols: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.num_rows = len(self.data)
        self.num_cols = len(self.data[0])

    def solve(self, row, col, direction) -> SolvedWorld:
        solved_world = SolvedWorld(self.num_rows, self.num_cols)
        active_lasers: list[tuple[int, int, int]] = [(row, col, direction)]
        while len(active_lasers) > 0:
            row, col, direction = active_lasers.pop(0)
            if self.is_oob(row, col):
                continue
            if solved_world.already_solved(row, col, direction):
                continue
            solved_world.add_laser(row, col, direction)

            contents = self.data[row][col]
            next_lasers = cell.next_lasers(contents, row, col, direction)
            active_lasers.extend(next_lasers)
        return solved_world

    def is_oob(self, row, col) -> bool:
        """true if laser is out of bounds"""
        return row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols


def get_input() -> World:
    """Read input file"""
    with open("input.txt") as file:
        all_cells: list[list[str]] = []
        for line in file:
            line = line.strip()
            all_cells.append(list(line))
        world = World(all_cells)
    return world


def solve_task(laser: tuple[int, int, int], world: World) -> int:
    """Calculates number of energized tiles"""
    return world.solve(*laser).num_energized()


def main() -> None:
    """main function"""

    world = get_input()

    # part 1
    laser = (0, 0, EAST)
    print(solve_task(laser, world))

    # part 2: brute force coz our impl is already cached/backtracked
    tasks = []
    for col in range(world.num_cols):
        tasks.append((0, col, SOUTH))
        tasks.append((world.num_rows - 1, col, NORTH))

    for row in range(world.num_rows):
        tasks.append((row, 0, EAST))
        tasks.append((row, world.num_cols - 1, WEST))
    start = time.time()
    print(max(solve_task(task, world) for task in tasks))
    print(time.time() - start)


if __name__ == "__main__":
    main()
