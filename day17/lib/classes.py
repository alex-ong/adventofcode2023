"""classes for day 17."""
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Optional

from day17.lib.direction import ALL_DIRECTIONS, Direction


@dataclass(order=True, frozen=True)
class Step:
    """Represents one "step", which could be a multi-step."""

    total_cost: int
    row: int
    col: int
    direction: Direction
    consecutive_steps: int

    src_step: Optional["Step"] = field(repr=False, hash=False)


class TileCache:
    """A cache of shortest routes to a tile from each direction."""

    cache: dict[Direction, list[Step | None]]
    cache_min: int  # min steps in direction
    cache_max: int  # max steps in direction

    def __init__(self, cache_min: int, cache_max: int):
        """Initialize the tile with an empty entry from each direction."""
        cache_length = cache_max - cache_min + 1
        self.cache = {key: [None] * cache_length for key in ALL_DIRECTIONS}
        self.cache_min = cache_min
        self.cache_max = cache_max

    def __getitem__(self, dir_steps: tuple[Direction, int]) -> Step | None:
        """Lookup our cache based on how many steps in one direction we took to get here."""
        direction, steps = dir_steps
        return self.cache[direction][steps - self.cache_min]

    def __setitem__(self, dir_steps: tuple[Direction, int], item: Step) -> None:
        """Set steps based on how many steps in one direction we took to get here."""
        direction, steps = dir_steps
        self.cache[direction][steps - self.cache_min] = item


class SolutionCache:
    """2d array of tilecaches."""

    cache: list[list[TileCache]]

    def __init__(self, num_rows: int, num_cols: int, cache_min: int, cache_max: int):
        """Generate empty tile cache."""
        self.cache = [
            [TileCache(cache_min, cache_max) for _ in range(num_cols)]
            for _ in range(num_rows)
        ]

    def add_solution(self, step: Step) -> bool:
        """Adds solution to cache returns whether an improvement was made."""
        tile_cache = self.cache[step.row][step.col]
        existing_item = tile_cache[step.direction, step.consecutive_steps]
        if existing_item is None:
            tile_cache[step.direction, step.consecutive_steps] = step
            return True

        # due to the way that we run in BFS, we shouldn't be getting
        # into this branch
        if step.total_cost < existing_item.total_cost:
            raise AssertionError("this shouldn't be possible")
            # tile_cache[step.direction, step.consecutive_steps] = step
            # return True
        return False


@dataclass
class WorldPart1:
    """World for part1."""

    costs: list[list[int]]
    num_rows: int = field(init=False)
    num_cols: int = field(init=False)

    def __post_init__(self) -> None:
        """Post initialize cached properties."""
        self.num_rows = len(self.costs)
        self.num_cols = len(self.costs[0])

    def __getitem__(self, row_col: tuple[int, int]) -> int | None:
        """Returns cost at given row/col."""
        row, col = row_col
        if self.is_oob(row, col):
            return None
        return self.costs[row][col]

    def create_step(self, step: Step, direction: Direction) -> Step | None:
        """Create step from previous step and a given direction.

        Returns None if the step is invalid or suboptimal
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
        """Solve using dynamic programming.

        Returns final step which contains src steps;
        so we have the entire path
        """
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

        raise AssertionError("No solution found!")

    def is_oob(self, row: int, col: int) -> bool:
        """Returns if we are out of bounds.

        Args:
            row (int): row to check
            col (int): col to check

        Returns:
            bool: if we are out of bounds.
        """
        return row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols


class WorldPart2(WorldPart1):
    """Extension of part1 with a few overrides."""

    def create_step(self, step: Step, direction: Direction) -> Step | None:
        """Create step from previous step and a given direction."""
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
        """Solve using DP.

        Returns final step which contains src steps;
        so we have the entire path
        """
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
        raise AssertionError("No solution found!")
