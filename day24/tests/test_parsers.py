from day24.day24 import INPUT_SMALL
from day24.lib.classes import Hailstone, Vector3
from day24.lib.parsers import parse_input, parse_vector3


def test_vector3() -> None:
    v1: Vector3 = parse_vector3(" 2, 4, 8")
    assert v1.x == 2
    assert v1.y == 4
    assert v1.z == 8

    v2: Vector3 = parse_vector3("3,5,-107")
    assert v2.x == 3
    assert v2.y == 5
    assert v2.z == -107


def test_parser() -> None:
    hailstones: list[Hailstone] = parse_input(INPUT_SMALL)

    assert len(hailstones) == 5
    assert hailstones[0].position == Vector3(19, 13, 30)
    assert hailstones[0].trajectory == Vector3(-2, 1, -2)

    assert hailstones[-1].position == Vector3(20, 19, 15)
    assert hailstones[-1].trajectory == Vector3(1, -5, -3)
