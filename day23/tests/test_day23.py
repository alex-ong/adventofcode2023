from typing import TYPE_CHECKING

from day23.day23 import INPUT_SMALL, part1, part2
from day23.lib.classes import Solver1
from day23.lib.parsers import get_maze

if TYPE_CHECKING:
    from day23.lib.classes import Maze, Path


def test_solver() -> None:
    maze: Maze = get_maze(INPUT_SMALL)

    solver = Solver1(maze)
    paths: list[Path] = solver.solve()

    path_lengths = [len(path) for path in paths]
    path_lengths.sort()

    assert path_lengths == [74, 82, 82, 86, 90, 94]


def test_part1() -> None:
    maze: Maze = get_maze(INPUT_SMALL)
    assert part1(maze) == 94


def test_part2() -> None:
    maze: Maze = get_maze(INPUT_SMALL)
    assert part2(maze) == 154
