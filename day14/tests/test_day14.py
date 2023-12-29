"""Tests for main day14 functions."""
from day14.day14 import (
    INPUT_SMALL,
    World,
    get_input,
    question1,
    question2,
    simulate_row,
)
from day14.lib.direction import Direction

INPUT_ARROW = "day14/input-arrow.txt"


def test_get_input() -> None:
    """Test ``get_input()``."""
    world: World = get_input(INPUT_SMALL)
    assert len(world.data) == 10  # rows
    assert len(world.data[0]) == 10  # cols


def test_questions() -> None:
    """Test main question functions."""
    world: World = get_input(INPUT_SMALL)
    assert question1(world) == 136
    assert question2(world) == 64


def test_simulate_row() -> None:
    """Test simulation of a row."""
    assert simulate_row(list("OO.#O....O"))[0] == list("OO.#OO....")
    assert simulate_row(list(".........O"))[0] == list("O.........")


def test_rotate_world() -> None:
    """Test rotating the world."""
    world: World = get_input(INPUT_ARROW)

    assert world.left_is == Direction.West

    ARROW_WEST = [
        (".", ".", ".", ".", ".", "."),
        (".", ".", ".", ".", ".", "."),
        (".", ".", "#", ".", ".", "."),
        (".", "#", "#", ".", ".", "."),
        ("#", "#", "#", "#", "#", "#"),
        (".", "#", "#", ".", ".", "."),
        (".", ".", "#", ".", ".", "."),
        (".", ".", ".", ".", ".", "."),
        (".", ".", ".", ".", ".", "."),
    ]
    assert world.rotate_world_ccw().data == ARROW_WEST
    assert world.rotate_world_ccw().left_is == Direction.North

    ARROW_SOUTH = [
        (".", ".", ".", ".", "#", ".", ".", ".", "."),
        (".", ".", ".", ".", "#", ".", ".", ".", "."),
        (".", ".", ".", ".", "#", ".", ".", ".", "."),
        (".", ".", "#", "#", "#", "#", "#", ".", "."),
        (".", ".", ".", "#", "#", "#", ".", ".", "."),
        (".", ".", ".", ".", "#", ".", ".", ".", "."),
    ]
    assert world.rotate_world_cw().rotate_world_cw().data == ARROW_SOUTH
    assert world.rotate_world_cw().rotate_world_cw().left_is == Direction.East

    ARROW_EAST = [
        (".", ".", ".", ".", ".", "."),
        (".", ".", ".", ".", ".", "."),
        (".", ".", ".", "#", ".", "."),
        (".", ".", ".", "#", "#", "."),
        ("#", "#", "#", "#", "#", "#"),
        (".", ".", ".", "#", "#", "."),
        (".", ".", ".", "#", ".", "."),
        (".", ".", ".", ".", ".", "."),
        (".", ".", ".", ".", ".", "."),
    ]

    assert world.rotate_world_cw().data == ARROW_EAST
    assert world.rotate_world_cw().left_is == Direction.South

    world1 = world.rotate_world_cw().rotate_world_ccw()
    world2 = world.rotate_world_ccw()
    world3 = world.rotate_world_cw()
    world4 = world.rotate_world_cw().rotate_world_cw()
    assert world1.as_orientiented_north() == world2.as_orientiented_north()
    assert world3.as_orientiented_north() == world4.as_orientiented_north()
    assert world4.as_orientiented_north() == world1.as_orientiented_north()
