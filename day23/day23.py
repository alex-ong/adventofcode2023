"""Day23 solution."""
from day23.lib.classes import Maze, Path, Solver1
from day23.lib.classes2 import Solver2
from day23.lib.parsers import get_maze

INPUT = "day23/input.txt"
INPUT_SMALL = "day23/input-small.txt"


def part1(maze: Maze) -> int:
    """Solve part1 (maximal distance given one-ways)."""
    solver = Solver1(maze, True)
    paths: list[Path] = solver.solve()
    paths.sort(key=lambda path: len(path), reverse=True)
    print(paths[0].overlay(maze))
    return len(paths[0])


def part2(maze: Maze) -> int:
    """Solve part2 (maximal distance, no one-ways)."""
    solver = Solver2(maze)
    return solver.solve()


def main() -> None:
    """Read data then solve part1/part2."""
    maze: Maze = get_maze(INPUT)

    print(part1(maze))
    print(part2(maze))


if __name__ == "__main__":
    main()
