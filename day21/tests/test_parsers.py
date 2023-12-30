"""Test day21 parsers."""
from day21.day21 import FILE_SMALL
from day21.lib.parsers import parse_maze


def test_parser() -> None:
    """Test ``parse_maze``."""
    start_pos, maze = parse_maze(FILE_SMALL)
    assert start_pos.col == 5
    assert start_pos.row == 5
    assert maze.num_cols == 11
    assert maze.num_cols == 11
