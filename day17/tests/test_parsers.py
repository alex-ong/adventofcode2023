"""Test parsing function."""
from day17.day17 import INPUT_SMALL
from day17.lib.parsers import get_input


def test_parser() -> None:
    """Test parsing function."""
    data: list[list[int]] = get_input(INPUT_SMALL)

    assert data[0] == [2, 4, 1, 3, 4, 3, 2, 3, 1, 1, 3, 2, 3]
    assert len(data) == 13
