from day16.lib.cells import (
    BackSlashCell,
    Cell,
    DashCell,
    DotCell,
    ForwardSlashCell,
    PipeCell,
)
from day16.lib.direction import Direction
from day16.lib.laser import Laser

WEST_LASER = Laser(5, 4, Direction.WEST)
EAST_LASER = Laser(5, 6, Direction.EAST)
NORTH_LASER = Laser(4, 5, Direction.NORTH)
SOUTH_LASER = Laser(6, 5, Direction.SOUTH)


def test_dotcell() -> None:
    laser: Laser = Laser(5, 5, Direction.NORTH)
    cell: Cell = DotCell()
    assert cell.next_lasers(laser) == [NORTH_LASER]

    laser.direction = Direction.EAST
    assert cell.next_lasers(laser) == [EAST_LASER]

    laser.direction = Direction.WEST
    assert cell.next_lasers(laser) == [WEST_LASER]

    laser.direction = Direction.SOUTH
    assert cell.next_lasers(laser) == [SOUTH_LASER]


def test_dashcell() -> None:
    laser: Laser = Laser(5, 5, Direction.NORTH)
    cell: Cell = DashCell()

    assert set(cell.next_lasers(laser)) == {WEST_LASER, EAST_LASER}

    laser.direction = Direction.EAST
    assert cell.next_lasers(laser) == [EAST_LASER]

    laser.direction = Direction.WEST
    assert cell.next_lasers(laser) == [WEST_LASER]

    laser.direction = Direction.SOUTH
    assert set(cell.next_lasers(laser)) == {WEST_LASER, EAST_LASER}


def test_pipecell() -> None:
    laser: Laser = Laser(5, 5, Direction.NORTH)
    cell: Cell = PipeCell()

    assert cell.next_lasers(laser) == [NORTH_LASER]

    laser.direction = Direction.EAST
    assert set(cell.next_lasers(laser)) == {NORTH_LASER, SOUTH_LASER}

    laser.direction = Direction.WEST
    assert set(cell.next_lasers(laser)) == {NORTH_LASER, SOUTH_LASER}

    laser.direction = Direction.SOUTH
    assert cell.next_lasers(laser) == [SOUTH_LASER]


def test_forwardslashcell() -> None:
    laser: Laser = Laser(5, 5, Direction.NORTH)
    cell: Cell = ForwardSlashCell()

    assert cell.next_lasers(laser) == [EAST_LASER]

    laser.direction = Direction.EAST
    assert cell.next_lasers(laser) == [NORTH_LASER]

    laser.direction = Direction.WEST
    assert cell.next_lasers(laser) == [SOUTH_LASER]

    laser.direction = Direction.SOUTH
    assert cell.next_lasers(laser) == [WEST_LASER]


def test_backslashcell() -> None:
    laser: Laser = Laser(5, 5, Direction.NORTH)
    cell: Cell = BackSlashCell()

    assert cell.next_lasers(laser) == [WEST_LASER]

    laser.direction = Direction.EAST
    assert cell.next_lasers(laser) == [SOUTH_LASER]

    laser.direction = Direction.WEST
    assert cell.next_lasers(laser) == [NORTH_LASER]

    laser.direction = Direction.SOUTH
    assert cell.next_lasers(laser) == [EAST_LASER]
