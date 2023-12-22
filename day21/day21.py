"""day21 solution"""

from queue import Queue
from typing import Optional

from lib.classes import (
    BaseDistanceMaze,
    DistanceMaze,
    DistanceMazes,
    Maze,
    Position,
    PositionDist,
)
from lib.parsers_21 import parse_maze

# first calculate minimum distance for every tile
# everything that is even, is a winner for 64
# there is no way to even get back onto an odd number. i am genius
# calculate if there is a cycle that lands on itself in an odd number of steps
# same for every tile i guess. DP weird champ

FILE_SMALL = "input-small.txt"
FILE_MAIN = "input.txt"
FILE_CLEANER = "input-cleaner.txt"
FILE = FILE_MAIN
STEPS = 64


def solve(start_pos: Position, maze: Maze, big: bool = False) -> int:
    print(start_pos)
    print(maze)

    nodes: Queue[PositionDist] = Queue()
    nodes.put(PositionDist(start_pos.row, start_pos.col, distance=0))
    distances: BaseDistanceMaze
    if big:
        distances = DistanceMaze(maze.num_rows, maze.num_cols)
    else:
        distances = DistanceMazes(maze.num_rows, maze.num_cols)

    print("before:")
    print(distances.overlay(maze))
    while True:
        pos: PositionDist = nodes.get()
        if pos.distance >= STEPS + 1:
            break
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
    print("after")
    print(distances.overlay(maze))
    print(distances.calc_steps())
    return 0


def main() -> None:
    start_pos, maze = parse_maze(FILE)
    solve(start_pos, maze)


if __name__ == "__main__":
    main()
