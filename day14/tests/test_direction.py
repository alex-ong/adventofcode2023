from day14.lib.direction import Direction


def test_direction() -> None:
    assert Direction.North.next_direction_cw() == Direction.East
    assert Direction.East.next_direction_cw() == Direction.South
    assert Direction.South.next_direction_cw() == Direction.West
    assert Direction.West.next_direction_cw() == Direction.North

    assert Direction.North.next_direction_ccw() == Direction.West
    assert Direction.East.next_direction_ccw() == Direction.North
    assert Direction.South.next_direction_ccw() == Direction.East
    assert Direction.West.next_direction_ccw() == Direction.South
