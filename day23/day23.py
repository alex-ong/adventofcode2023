from day23.lib.classes import Maze, Path, Solver, Solver1
from day23.lib.classes2 import Solver2
from day23.lib.parsers import get_maze

INPUT = "day23/input.txt"
INPUT_SMALL = "day23/input-small.txt"


def part1(maze: Maze) -> int:
    solver = Solver1(maze, True)
    return run_solver(solver)


def part2(maze: Maze) -> int:
    solver = Solver2(maze)
    return run_solver(solver)


def run_solver(solver: Solver) -> int:
    paths: list[Path] = solver.solve()
    path_lengths = [len(path) for path in paths]
    path_lengths.sort(reverse=True)
    return path_lengths[0]


def main() -> None:
    maze: Maze = get_maze(INPUT_SMALL)

    # print(part1(maze))
    print(part2(maze))


if __name__ == "__main__":
    main()
