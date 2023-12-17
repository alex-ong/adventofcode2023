"""
day16 solution
"""


import time
from dataclasses import dataclass

from cells import Cell
from direction import Direction
from laser import LaserInstance


class SolvedWorld:
    data: list[list[list[LaserInstance]]]

    def __init__(self, num_rows, num_cols):
        self.data = [[[] for _ in range(num_cols)] for _ in range(num_rows)]

    def already_solved(self, laser: LaserInstance) -> bool:
        """returns true if laser already calculated"""
        solutions = self.data[laser.row][laser.col]
        if laser in solutions:
            return True
        return False

    def add_laser(self, laser: LaserInstance):
        """adds laser to cell"""
        solutions = self.data[laser.row][laser.col]
        solutions.append(laser)

    def __str__(self):
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
    data: list[list[Cell]]

    @property
    def num_rows(self) -> int:
        """return number of rows"""
        return len(self.data)

    @property
    def num_cols(self) -> int:
        """Return number of columns"""
        return len(self.data[0])

    def solve(self, start_laser=LaserInstance(0, 0, Direction.EAST)) -> SolvedWorld:
        solved_world = SolvedWorld(self.num_rows, self.num_cols)
        active_lasers = [start_laser]
        while len(active_lasers) > 0:
            laser = active_lasers.pop(0)
            if self.is_oob(laser):
                continue
            if solved_world.already_solved(laser):
                continue
            solved_world.add_laser(laser)

            cell: Cell = self.data[laser.row][laser.col]
            next_lasers = cell.next_lasers(laser)
            active_lasers.extend(next_lasers)
        return solved_world

    def is_oob(self, laser):
        """true if laser is out of bounds"""
        return (
            laser.row < 0
            or laser.row >= self.num_rows
            or laser.col < 0
            or laser.col >= self.num_cols
        )


def get_input() -> World:
    """Read input file"""
    with open("input.txt") as file:
        all_cells: list[list[Cell]] = []
        for line in file:
            line = line.strip()
            cells = [Cell.construct(char) for char in line]
            all_cells.append(cells)
        world = World(all_cells)
    return world


def solve_task(task: LaserInstance, world: World):
    """Calculates number of energized tiles"""
    return world.solve(task).num_energized()


def main():
    """main function"""

    world = get_input()

    # part 1
    solved_world = world.solve()
    print(solved_world.num_energized())

    # part 2: brute force coz our impl is already cached/backtracked
    tasks = []
    for col in range(world.num_cols):
        tasks.append(LaserInstance(0, col, Direction.SOUTH))
        tasks.append(LaserInstance(world.num_rows - 1, col, Direction.NORTH))

    for row in range(world.num_rows):
        tasks.append(LaserInstance(row, 0, Direction.EAST))
        tasks.append(LaserInstance(row, world.num_cols - 1, Direction.WEST))

    start = time.time()
    print(max(solve_task(task, world) for task in tasks))
    print(f"time: {time.time() - start}")


if __name__ == "__main__":
    main()
