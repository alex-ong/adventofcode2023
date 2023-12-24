from day24.day24 import INPUT_SMALL, get_intersection_2d, part1, within_2d
from day24.lib.classes import Hailstone, Vector2, Vector3
from day24.lib.parsers import parse_input


def test_part1() -> None:
    file_path, valid_range = INPUT_SMALL
    hailstones: list[Hailstone] = parse_input(file_path)
    assert part1(hailstones, valid_range) == 2


def test_get_intersection_2d() -> None:
    hailstone_a = Hailstone(Vector3(20, 25, 34), Vector3(-2, -2, -4))
    hailstone_b = Hailstone(Vector3(12, 31, 28), Vector3(-1, -2, -1))

    assert get_intersection_2d(hailstone_a, hailstone_b) == Vector2(-2, 3)


def test_within_2d() -> None:
    valid_range = Vector2(7, 27)
    v1 = Vector2(14 + 1 / 3, 15 + 1 / 3)
    v2 = Vector2(11 + 6 / 9, 16 + 6 / 9)
    v3 = Vector2(6.2, 19.4)
    v4 = Vector2(-6, -5)
    v5 = Vector2(-2, 3)
    assert within_2d(v1, valid_range)
    assert within_2d(v2, valid_range)
    assert not within_2d(v3, valid_range)
    assert not within_2d(v4, valid_range)
    assert not within_2d(v5, valid_range)
