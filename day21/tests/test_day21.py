import pytest

from day21.day21 import FILE_SMALL, solve
from day21.lib.parsers import parse_maze

INPUT_11x11 = "day21/tests/input-11x11.txt"
INPUT_5x5 = "day21/tests/input-5x5.txt"


def test_day21() -> None:
    start_pos, maze = parse_maze(FILE_SMALL)

    assert solve(start_pos, maze, 6) == 16
    assert solve(start_pos, maze, 30) == 42

    start_pos, maze = parse_maze(INPUT_5x5)
    with pytest.raises(ValueError):
        solve(start_pos, maze, maze.num_rows, True)

    assert solve(start_pos, maze, int(maze.num_rows * 3.5), True) == 324
    assert solve(start_pos, maze, int(maze.num_rows * 4.5), True) == 529

    start_pos, maze = parse_maze(INPUT_11x11)
    with pytest.raises(ValueError):
        solve(start_pos, maze, maze.num_rows, True)

    assert solve(start_pos, maze, int(maze.num_rows * 3.5), True) == 1521
    assert solve(start_pos, maze, int(maze.num_rows * 4.5), True) == 2500

    assert solve(start_pos, maze, int(maze.num_rows * 3.5), True, False) == 1521
