"""day21 solution"""

from queue import Queue

from lib.classes import DistanceMaze, Maze, Position, PositionDist
from lib.parsers_21 import parse_maze

# first calculate minimum distance for every tile
# everything that is even, is a winner for 64
# there is no way to even get back onto an odd number. i am genius
# calculate if there is a cycle that lands on itself in an odd number of steps
# same for every tile i guess. DP weird champ

FILE_SMALL = "input-small.txt"
FILE_MAIN = "input.txt"
FILE = FILE_SMALL


def solve(start_pos: Position, maze: Maze) -> int:
    print(start_pos)
    print(maze)

    nodes: Queue[PositionDist] = Queue()
    nodes.put(PositionDist(start_pos.row, start_pos.col, distance=0))
    distances = DistanceMaze(maze.num_rows, maze.num_cols)
    print("")
    print(distances)
    while True:
        pos: PositionDist = nodes.get()
        if pos.distance >= 13:
            break
        # expand
        distance = distances[pos]
        maze_node = maze[pos]

        if distance is None:  # oob
            continue
        if distance != -1:  # already explored
            continue
        if maze_node == "#":  # hitting a wall
            continue
        # undiscovered!
        distances[pos] = pos.distance
        nodes.put(pos.replace(row=pos.row + 1))  # south
        nodes.put(pos.replace(row=pos.row - 1))  # north
        nodes.put(pos.replace(col=pos.col + 1))  # east
        nodes.put(pos.replace(col=pos.col - 1))  # west

    print()
    print(distances)
    print(distances.calc_steps())
    return 0


def main() -> None:
    start_pos, maze = parse_maze(FILE)
    solve(start_pos, maze)


if __name__ == "__main__":
    main()
