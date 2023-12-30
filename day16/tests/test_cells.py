"""Tests for each cell."""
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


def test_cell() -> None:
    """Tests ``Cell.construct()``."""
    dot_cell = Cell.construct(".")
    assert isinstance(dot_cell, DotCell)

    dash_cell = Cell.construct("-")
    assert isinstance(dash_cell, DashCell)

    pipe_cell = Cell.construct("|")
    assert isinstance(pipe_cell, PipeCell)

    fslash_cell = Cell.construct("/")
    assert isinstance(fslash_cell, ForwardSlashCell)

    bslash_cell = Cell.construct("\\")
    assert isinstance(bslash_cell, BackSlashCell)


def test_dotcell() -> None:
    """Test ``DotCell``."""
    laser: Laser = Laser(5, 5, Direction.NORTH)
    cell: Cell = DotCell(".")
    assert cell.next_lasers(laser) == [NORTH_LASER]

    laser = Laser(5, 5, Direction.EAST)
    assert cell.next_lasers(laser) == [EAST_LASER]

    laser = Laser(5, 5, Direction.WEST)
    assert cell.next_lasers(laser) == [WEST_LASER]

    laser = Laser(5, 5, Direction.SOUTH)
    assert cell.next_lasers(laser) == [SOUTH_LASER]


def test_dashcell() -> None:
    """Test ``DashCell``."""
    laser: Laser = Laser(5, 5, Direction.NORTH)
    cell: Cell = DashCell("-")

    assert set(cell.next_lasers(laser)) == {WEST_LASER, EAST_LASER}

    laser = Laser(5, 5, Direction.EAST)
    assert cell.next_lasers(laser) == [EAST_LASER]

    laser = Laser(5, 5, Direction.WEST)
    assert cell.next_lasers(laser) == [WEST_LASER]

    laser = Laser(5, 5, Direction.SOUTH)
    assert set(cell.next_lasers(laser)) == {WEST_LASER, EAST_LASER}


def test_pipecell() -> None:
    """Test ``PipeCell``."""
    laser: Laser = Laser(5, 5, Direction.NORTH)
    cell: Cell = PipeCell("|")

    assert cell.next_lasers(laser) == [NORTH_LASER]

    laser = Laser(5, 5, Direction.EAST)
    assert set(cell.next_lasers(laser)) == {NORTH_LASER, SOUTH_LASER}

    laser = Laser(5, 5, Direction.WEST)
    assert set(cell.next_lasers(laser)) == {NORTH_LASER, SOUTH_LASER}

    laser = Laser(5, 5, Direction.SOUTH)
    assert cell.next_lasers(laser) == [SOUTH_LASER]


def test_forwardslashcell() -> None:
    """Test ``ForwardSlashCell``."""
    laser: Laser = Laser(5, 5, Direction.NORTH)
    cell: Cell = ForwardSlashCell("/")

    assert cell.next_lasers(laser) == [EAST_LASER]

    laser = Laser(5, 5, Direction.EAST)
    assert cell.next_lasers(laser) == [NORTH_LASER]

    laser = Laser(5, 5, Direction.WEST)
    assert cell.next_lasers(laser) == [SOUTH_LASER]

    laser = Laser(5, 5, Direction.SOUTH)
    assert cell.next_lasers(laser) == [WEST_LASER]


def test_backslashcell() -> None:
    """Test ``BackSlashCell``."""
    laser: Laser = Laser(5, 5, Direction.NORTH)
    cell: Cell = BackSlashCell("\\")

    assert cell.next_lasers(laser) == [WEST_LASER]

    laser = Laser(5, 5, Direction.EAST)
    assert cell.next_lasers(laser) == [SOUTH_LASER]

    laser = Laser(5, 5, Direction.WEST)
    assert cell.next_lasers(laser) == [NORTH_LASER]

    laser = Laser(5, 5, Direction.SOUTH)
    assert cell.next_lasers(laser) == [EAST_LASER]
