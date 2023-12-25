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
    world: World = get_input(INPUT_SMALL)
    assert len(world.data) == 10  # rows
    assert len(world.data[0]) == 10  # cols


def test_questions() -> None:
    world: World = get_input(INPUT_SMALL)
    assert question1(world) == 136
    assert question2(world) == 64


def test_simulate_row() -> None:
    assert simulate_row(list("OO.#O....O"))[0] == list("OO.#OO....")
    assert simulate_row(list(".........O"))[0] == list("O.........")


def test_rotate_world() -> None:
    world: World = get_input(INPUT_ARROW)

    assert world.rotate_world_ccw().left_is == Direction.North
