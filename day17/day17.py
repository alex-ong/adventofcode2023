"""day17 solution"""
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Optional

from direction import ALL_DIRECTIONS, Direction


@dataclass(order=True)
class Step:
    total_cost: int
    row: int
    col: int
    direction: Direction
    consecutive_steps: int

    src_step: Optional["Step"] = field(repr=False)

    def __hash__(self):
        items = [
            self.total_cost,
            self.row,
            self.col,
            self.direction,
            self.consecutive_steps,
        ]
        return hash("|".join(str(item for item in items)))


class TileCache:
    def __init__(self):
        self.cache = {
            Direction.NORTH: [None, None, None],
            Direction.EAST: [None, None, None],
            Direction.SOUTH: [None, None, None],
            Direction.WEST: [None, None, None],
        }

    def __getitem__(self, dir_steps: tuple[Direction, int]):
        direction, steps = dir_steps
        return self.cache[direction][steps - 1]

    def __setitem__(self, dir_steps: tuple[Direction, int], item):
        direction, steps = dir_steps
        self.cache[direction][steps - 1] = item


class SolutionCache:
    cache: list[list[TileCache]]

    def __init__(self, num_rows, num_cols):
        self.cache = [[TileCache() for _ in range(num_cols)] for _ in range(num_rows)]

    def add_solution(self, step):
        """adds solution to cache"""
        tile_cache = self.cache[step.row][step.col]
        existing_item = tile_cache[step.direction, step.consecutive_steps]
        if existing_item is None:
            tile_cache[step.direction, step.consecutive_steps] = step
            return True

        if step.total_cost < existing_item.total_cost:
            tile_cache[step.direction, step.consecutive_steps] = step
            return True
        return False


@dataclass
class World:
    costs: list[list[int]]

    num_rows: int = field(init=False)
    num_cols: int = field(init=False)

    def __post_init__(self):
        self.num_rows = len(self.costs)
        self.num_cols = len(self.costs[0])

    def __getitem__(self, row_col):
        row, col = row_col
        if self.is_oob(row, col):
            return None
        return self.costs[row][col]

    def create_step(self, step: Step, direction: Direction):
        """Create step from previous step and a given direction"""
        row, col = direction.offset(step.row, step.col)
        if (cost := self[row, col]) is None:
            return None

        if direction == step.direction.opposite():
            return None
        if direction == step.direction:
            consecutive = step.consecutive_steps + 1
            if consecutive > 3:
                return None
        else:
            consecutive = 1

        return Step(step.total_cost + cost, row, col, direction, consecutive, step)

    def solve(self):
        # we need to do this via DP
        solution_cache = SolutionCache(self.num_rows, self.num_cols)
        step: Step = Step(0, 0, 0, Direction.NORTH, 0, None)
        steps_to_explore: PriorityQueue[Step] = PriorityQueue()
        steps_to_explore.put(step)

        while not steps_to_explore.empty():
            step = steps_to_explore.get()
            if step.row == self.num_rows - 1 and step.col == self.num_cols - 1:
                return step  # result!
            if not solution_cache.add_solution(step):
                continue

            for direction in ALL_DIRECTIONS:
                if (new_step := self.create_step(step, direction)) is not None:
                    steps_to_explore.put(new_step)

    def is_oob(self, row: int, col: int):
        """true if laser is out of bounds"""
        return row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols


def get_input():
    """Convert input into world dataclass"""
    with open("input.txt", "r", encoding="utf8") as file:
        data: list[list[int]] = []
        for line in file:
            data.append([int(char) for char in line.strip()])
        return World(data)


def main():
    """mainfunc"""
    world: World = get_input()

    # q1
    result = world.solve()
    world_string = [[str(val) for val in row] for row in world.costs]

    step = result
    while step is not None:
        world_string[step.row][step.col] = str(step.direction)
        print(step.row, step.col, step.total_cost)
        step = step.src_step

    print("\n".join("".join(val for val in row) for row in world_string))
    print(result)


if __name__ == "__main__":
    main()
