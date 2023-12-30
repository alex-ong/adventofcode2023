"""Tests for day23 classes."""
import pytest

from day23.day23 import INPUT_SMALL
from day23.lib.classes import Maze, Path, Position, Solver1, generate_paths
from day23.lib.parsers import get_maze


def test_position() -> None:
    """Test ``Position`` class."""
    pos: Position = Position(0, 0)
    pos2 = pos.copy_modify()
    assert pos == pos2
    pos3 = pos.copy_modify(row=1)
    assert pos3.row == 1 and pos3.col == 0
    pos4 = pos.copy_modify(col=1)
    assert pos4.row == 0 and pos4.col == 1


def test_maze() -> None:
    """Test ``Maze`` class."""
    maze: Maze = get_maze(INPUT_SMALL)
    assert maze[Position(0, 0)] == "#"
    assert maze[Position(0, 1)] == "."
    assert maze[Position(-1, 0)] is None

    position_checks = [
        (Position(0, 1), 1),
        (Position(1, 1), 2),
        (Position(3, 11), 3),
        (Position(5, 3), 3),
    ]

    for pos, result in position_checks:
        print(pos, result)
        assert maze.get_cell_branches(pos) == result


def test_solver1() -> None:
    """Test ``Solver`` class."""
    maze: Maze = get_maze(INPUT_SMALL)
    solver: Solver1 = Solver1(maze)

    expands = [
        (
            Position(5, 5),
            " ",
            {Position(4, 5), Position(6, 5), Position(5, 4), Position(5, 6)},
        ),
        (Position(5, 5), "^", {Position(4, 5)}),
        (Position(5, 5), ">", {Position(5, 6)}),
        (Position(5, 5), "<", {Position(5, 4)}),
        (Position(5, 5), "v", {Position(6, 5)}),
    ]

    for pos, tile, result in expands:
        assert set(solver.expand_hill(pos, tile)) == result

    # solve part2 naively, to make sure the code works
    maze = get_maze(INPUT_SMALL)
    solver1b: Solver1 = Solver1(maze, handle_hills=False)
    paths = solver1b.solve()
    path_lengths = [len(path) for path in paths]
    path_lengths.sort(reverse=True)
    assert path_lengths[0] == 154


def test_path() -> None:
    """Test ``Path`` class."""
    path = Path()

    # assert that path.last() fails when calling on empty path
    with pytest.raises(ValueError):
        path.last()
    path.add(Position(0, 0))
    path.add(Position(0, 1))
    assert path.last() == Position(0, 1)

    path2 = path.copy()

    assert path2.last() == Position(0, 1)
    path2.add(Position(0, 2))
    assert path.last() == Position(0, 1)
    assert path2.last() == Position(0, 2)


def test_generate_paths() -> None:
    """Test ``generate_paths()``."""
    path = Path()
    path.add(Position(0, 0))
    path.add(Position(0, 1))

    # manually generate the paths
    path1 = path.copy()
    path1.add(Position(0, 2))
    path2 = path.copy()
    path2.add(Position(-1, 1))

    # note that the original path is modified in-place!
    paths: list[Path] = generate_paths(path, [Position(0, 2), Position(-1, 1)])
    assert len(paths) == 2

    auto_path1 = paths[0]
    auto_path2 = paths[1]
    assert {auto_path1, auto_path2} == {path1, path2}

    paths = generate_paths(path, [])
    assert (len(paths)) == 0

    # test that we modify the path inplace when passed one position
    path_before = path  # reference
    len_before = len(path_before.route)
    paths = generate_paths(path, [Position(69, 69)])
    assert (
        len(paths) == 1
        and paths[0] == path_before
        and len(path_before.route) == len(paths[0].route)
        and len_before + 1 == len(path_before.route)
    )
