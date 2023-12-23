from day23.lib.classes import Maze, Path, Solver1
from day23.lib.classes2 import Solver2
from day23.lib.parsers import get_maze

INPUT = "day23/input.txt"
INPUT_SMALL = "day23/input-small.txt"


def part1(maze: Maze) -> int:
    solver = Solver1(maze, True)
    paths: list[Path] = solver.solve()
    path_lengths = [len(path) for path in paths]
    path_lengths.sort(reverse=True)
    return path_lengths[0]


def part2(maze: Maze) -> int:
    solver = Solver2(maze)
    return solver.solve()


def main() -> None:
    maze: Maze = get_maze(INPUT)

    print(part1(maze))
    print(part2(maze))


if __name__ == "__main__":
    main()
