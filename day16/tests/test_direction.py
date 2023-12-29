"""Test direction."""
from day16.lib.direction import Direction


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
