from typing import TYPE_CHECKING

from day23.day23 import INPUT_SMALL
from day23.lib.parsers import get_maze

if TYPE_CHECKING:
    from day23.lib.classes import Maze


def test_get_maze() -> None:
    maze: Maze = get_maze(INPUT_SMALL)
    assert maze.num_rows == 23
    assert maze.num_cols == 23
