"""day21 solution"""

from dataclasses import dataclass
from queue import Queue
from typing import Optional

from day21.lib.classes import (
    BaseDistanceMaze,
    DistanceMaze,
    DistanceMazes,
    GiantNodeParser,
    GiantNodeType,
    Maze,
    Position,
    PositionDist,
)
from day21.lib.parsers import parse_maze

# first calculate minimum distance for every tile
# everything that is even, is a winner for 64
# there is no way to even get back onto an odd number. i am genius
# calculate if there is a cycle that lands on itself in an odd number of steps
# same for every tile i guess. DP weird champ

FILE_SMALL = "day21/input-small.txt"
FILE_MAIN = "day21/input.txt"
FILE = FILE_MAIN


GIGA_TARGET = 26_501_365  # even parity


def mini_solve(
    start_pos: Position, maze: Maze, steps: int, distances: BaseDistanceMaze
) -> BaseDistanceMaze:
    """given a basedistanceMaze, runs `steps` steps then returns the maze"""
    nodes: Queue[PositionDist] = Queue()
    nodes.put(PositionDist(start_pos.row, start_pos.col, distance=0))

    distance_reached: bool = False
    while not nodes.empty() and not distance_reached:
        pos: PositionDist = nodes.get()
        if pos.distance >= steps + 1:
            distance_reached = True
            continue
        # expand
        distance: Optional[int] = distances[pos]
        maze_node: Optional[str] = maze[pos]

        if distance is None:  # oob
            continue
        if distance != -1:  # already explored
            continue
        if maze_node == "#":  # hitting a wall
            continue
        # undiscovered!
        distances[pos] = pos.distance

        south = pos.replace(row=pos.row + 1)
        north = pos.replace(row=pos.row - 1)
        east = pos.replace(col=pos.col + 1)
        west = pos.replace(col=pos.col - 1)

        for direction in [north, south, east, west]:
            nodes.put(direction)
    return distances


@dataclass
class SmartSteps:
    boards_to_edge: int
    steps: int


def naive_solve(
    start_pos: Position, maze: Maze, steps: int, distances: BaseDistanceMaze
) -> int:
    distances = mini_solve(start_pos, maze, steps, distances)
    print(distances.overlay(maze))
    return distances.calc_steps(steps % 2)


def calculate_smart_steps(board_size: int, steps: int) -> SmartSteps:
    """Given a board size and num steps, calculate how many steps we actually need"""
    steps_remaining = steps % board_size
    if steps_remaining != board_size // 2:
        raise ValueError("big mode only supported for steps_remaining == maze_rows//2")
    boards_to_edge = steps // board_size
    print("boards_to_edge", boards_to_edge)

    if boards_to_edge % 2 == 0:
        sim_steps = board_size * 2 + steps_remaining
    else:
        sim_steps = board_size * 3 + steps_remaining
    return SmartSteps(boards_to_edge, sim_steps)


# FILE_MAIN is 131 x 131.
# This means  we need 130 steps(?) to hit the corners,
# and 131 to get to next centre
def solve(
    start_pos: Position,
    maze: Maze,
    steps: int,
    unlimited_map: bool = False,
    brute_force: bool = False,  # for > 3 boards wide, use smart algo
) -> int:
    distances: BaseDistanceMaze

    if unlimited_map:
        distances = DistanceMazes(maze.num_rows, maze.num_cols)
    else:  # small
        distances = DistanceMaze(maze.num_rows, maze.num_cols)

    # if we are small, or havent got smart_solve enabled, brute force it.
    if not unlimited_map or (unlimited_map and brute_force):
        return naive_solve(start_pos, maze, steps, distances)

    smart_steps: SmartSteps = calculate_smart_steps(maze.num_rows, steps)
    distances = mini_solve(start_pos, maze, smart_steps.steps, distances)

    if maze.num_cols <= 5:
        distances.overlay(maze)

    if not isinstance(distances, DistanceMazes):
        raise AssertionError("ya done goof here")
    giant_parser = GiantNodeParser(distances, smart_steps.boards_to_edge)
    remainder = steps % 2
    result = 0
    for node_type in GiantNodeType:
        node = giant_parser.get_node(node_type)
        node_steps = node.calc_steps(remainder)
        node_count = giant_parser.get_node_count(node_type)
        node_type_steps = node_steps * node_count
        print(f"{node_type.name}, count: {node_count}, steps: {node_steps}")
        result += node_type_steps

    return result


def main() -> None:
    start_pos, maze = parse_maze(FILE)
    # part1
    print(solve(start_pos, maze, 64))

    # part2
    print(solve(start_pos, maze, GIGA_TARGET, True, False))


if __name__ == "__main__":
    main()
