"""Test classes for day21."""
import pytest

from day21.lib.classes import (
    DistanceMaze,
    DistanceMazes,
    GiantNodeParser,
    Maze,
    Position,
    PositionDist,
)


def test_position() -> None:
    """Test ``Position`` class."""
    position: Position = Position(21, 22)
    assert str(position) == "21, 22"


def test_position_dist() -> None:
    """Test ``PositionDist`` class."""
    pos_dist = PositionDist(21, 22, distance=69)
    assert str(pos_dist) == "21, 22, d=69"


def test_maze() -> None:
    """Test ``Maze`` class."""
    maze: Maze = Maze(["...", ".S.", "..."])

    assert str(maze) == "...\n.S.\n..."


def test_distance_maze() -> None:
    """Test ``DistanceMaze`` class."""
    maze: DistanceMaze = DistanceMaze(5, 5)
    maze[Position(69, 69)] = 22
    assert maze[Position(69, 69)] is None


def test_giant_node_parser() -> None:
    """Test ``GiantNodeParser`` class."""
    with pytest.raises(ValueError):
        GiantNodeParser(DistanceMazes(5, 5), 2)
