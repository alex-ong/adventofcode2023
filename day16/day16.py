"""
day16 solution
"""


from dataclasses import dataclass, field

from day16.lib.cells import Cell
from day16.lib.direction import Direction
from day16.lib.laser import Laser


class SolvedWorld:
    data: list[list[list[Laser]]]

    def __init__(self, num_rows: int, num_cols: int):
        self.data = [[[] for _ in range(num_cols)] for _ in range(num_rows)]

    def already_solved(self, laser: Laser) -> bool:
        """returns true if laser already calculated"""
        solutions = self.data[laser.row][laser.col]
        if laser in solutions:
            return True
        return False

    def add_laser(self, laser: Laser) -> None:
        """adds laser to cell"""
        solutions = self.data[laser.row][laser.col]
        solutions.append(laser)

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
    data: list[list[Cell]]

    num_rows: int = field(init=False, repr=False)
    num_cols: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.num_rows = len(self.data)
        self.num_cols = len(self.data[0])

    def solve(self, start_laser: Laser) -> SolvedWorld:
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

    def is_oob(self, laser: Laser) -> bool:
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


def solve_task(task: Laser, world: World) -> int:
    """Calculates number of energized tiles"""
    return world.solve(task).num_energized()


def main() -> None:
    """main function"""

    world = get_input()

    # part 1
    laser = Laser(0, 0, Direction.EAST)
    solved_world = world.solve(laser)
    print(solved_world.num_energized())

    # part 2: brute force coz our impl is already cached/backtracked
    tasks = []
    for col in range(world.num_cols):
        tasks.append(Laser(0, col, Direction.SOUTH))
        tasks.append(Laser(world.num_rows - 1, col, Direction.NORTH))

    for row in range(world.num_rows):
        tasks.append(Laser(row, 0, Direction.EAST))
        tasks.append(Laser(row, world.num_cols - 1, Direction.WEST))

    print(max(solve_task(task, world) for task in tasks))


if __name__ == "__main__":
    main()
