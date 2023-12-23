"""day17 solution"""
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Optional

from colorama import Back

from day17.lib.direction import ALL_DIRECTIONS, Direction


@dataclass(order=True)
class Step:
    total_cost: int
    row: int
    col: int
    direction: Direction
    consecutive_steps: int

    src_step: Optional["Step"] = field(repr=False)

    def __hash__(self) -> int:
        items = [
            self.total_cost,
            self.row,
            self.col,
            self.direction,
            self.consecutive_steps,
        ]
        return hash("|".join(str(item for item in items)))


class TileCache:
    cache: dict[Direction, list[Step | None]]
    cache_min: int
    cache_max: int

    def __init__(self, cache_min: int, cache_max: int):
        cache_length = cache_max - cache_min + 1
        self.cache = {key: [None] * cache_length for key in ALL_DIRECTIONS}
        self.cache_min = cache_min
        self.cache_max = cache_max

    def __getitem__(self, dir_steps: tuple[Direction, int]) -> Step | None:
        direction, steps = dir_steps
        return self.cache[direction][steps - self.cache_min]

    def __setitem__(self, dir_steps: tuple[Direction, int], item: Step) -> None:
        direction, steps = dir_steps
        self.cache[direction][steps - self.cache_min] = item


class SolutionCache:
    cache: list[list[TileCache]]

    def __init__(self, num_rows: int, num_cols: int, cache_min: int, cache_max: int):
        self.cache = [
            [TileCache(cache_min, cache_max) for _ in range(num_cols)]
            for _ in range(num_rows)
        ]

    def add_solution(self, step: Step) -> bool:
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
class WorldPart1:
    costs: list[list[int]]
    num_rows: int = field(init=False)
    num_cols: int = field(init=False)

    def __post_init__(self) -> None:
        self.num_rows = len(self.costs)
        self.num_cols = len(self.costs[0])

    def __getitem__(self, row_col: tuple[int, int]) -> int | None:
        """Returns cost at given row/col"""
        row, col = row_col
        if self.is_oob(row, col):
            return None
        return self.costs[row][col]

    def create_step(self, step: Step, direction: Direction) -> Step | None:
        """
        Create step from previous step and a given direction
        returns None if the step is invalid or suboptimal
        """
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

    def solve(self) -> Step:
        # we need to do this via DP
        solution_cache = SolutionCache(self.num_rows, self.num_cols, 1, 3)
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

        raise ValueError("No solution found!")

    def is_oob(self, row: int, col: int) -> bool:
        """true if laser is out of bounds"""
        return row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols


class WorldPart2(WorldPart1):
    """Extension of part1 with a few overrides"""

    def create_step(self, step: Step, direction: Direction) -> Step | None:
        """Create step from previous step and a given direction"""
        if direction == step.direction.opposite():
            return None
        if direction == step.direction:
            row, col = direction.offset(step.row, step.col)
            cost = self[row, col]
            if cost is None:
                return None
            consecutive = step.consecutive_steps + 1
            if consecutive > 10:
                return None
            return Step(step.total_cost + cost, row, col, direction, consecutive, step)
        else:
            consecutive = 4
            row_cols = direction.offset_list(step.row, step.col)
            multi_cost = 0
            for row_col in row_cols:
                row, col = row_col
                cost = self[row, col]
                if cost is None:
                    return None
                multi_cost += cost

            return Step(
                step.total_cost + multi_cost, row, col, direction, consecutive, step
            )

    def solve(self) -> Step:
        # we need to do this via DP
        solution_cache = SolutionCache(self.num_rows, self.num_cols, 4, 10)
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
        raise ValueError("No solution found!")


def get_input() -> list[list[int]]:
    """Convert input into world dataclass"""
    with open("input.txt", "r", encoding="utf8") as file:
        data: list[list[int]] = []
        for line in file:
            data.append([int(char) for char in line.strip()])
        return data


def solve_and_print(world: WorldPart1) -> None:
    """Solve and print"""
    result = world.solve()
    world_string = [[str(val) for val in row] for row in world.costs]

    step: Optional[Step] = result
    while step is not None:
        output_str = Back.GREEN + str(step.direction) + Back.BLACK
        world_string[step.row][step.col] = output_str
        step = step.src_step

    print("\n".join("".join(val for val in row) for row in world_string))
    print(result)


def main() -> None:
    """mainfunc"""
    # q1
    world: WorldPart1 = WorldPart1(get_input())
    solve_and_print(world)

    # q2
    world2: WorldPart2 = WorldPart2(get_input())
    solve_and_print(world2)


if __name__ == "__main__":
    main()
