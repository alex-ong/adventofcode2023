"""Tests for direction class."""
from day10.lib.direction import Direction


def test_direction() -> None:
    """Test direction class."""
    assert Direction.EAST.opposite() == Direction.WEST
    assert Direction.WEST.opposite() == Direction.EAST
    assert Direction.NORTH.opposite() == Direction.SOUTH
    assert Direction.SOUTH.opposite() == Direction.NORTH
