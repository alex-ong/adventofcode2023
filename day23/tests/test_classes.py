from day23.day23 import INPUT_SMALL
from day23.lib.classes import Maze, Position
from day23.lib.parsers import get_maze


def test_position() -> None:
    pos: Position = Position(0, 0)
    pos2 = pos.copy_modify()
    assert pos == pos2
    pos3 = pos.copy_modify(row=1)
    assert pos3.row == 1 and pos3.col == 0
    pos4 = pos.copy_modify(col=1)
    assert pos4.row == 0 and pos4.col == 1


def test_maze() -> None:
    maze: Maze = get_maze(INPUT_SMALL)
    assert maze[Position(0, 0)] == "#"
    assert maze[Position(0, 1)] == "."
    assert maze[Position(-1, 0)] is None
