"""Test direction class."""
from day17.lib.direction import Direction


def test_direction() -> None:
    """Test ``Direction`` class."""
    assert Direction.WEST.opposite() == Direction.EAST
    assert Direction.EAST.opposite() == Direction.WEST
    assert Direction.SOUTH.opposite() == Direction.NORTH
    assert Direction.NORTH.opposite() == Direction.SOUTH

    assert Direction.EAST.offset(0, 0) == (0, 1)
    assert Direction.WEST.offset(0, 0) == (0, -1)
    assert Direction.NORTH.offset(0, 0) == (-1, 0)
    assert Direction.SOUTH.offset(0, 0) == (1, 0)

    assert Direction.EAST.offset_list(0, 0) == [(0, 1), (0, 2), (0, 3), (0, 4)]
    assert Direction.WEST.offset_list(0, 0) == [(0, -1), (0, -2), (0, -3), (0, -4)]
    assert Direction.NORTH.offset_list(0, 0) == [(-1, 0), (-2, 0), (-3, 0), (-4, 0)]
    assert Direction.SOUTH.offset_list(0, 0) == [(1, 0), (2, 0), (3, 0), (4, 0)]
