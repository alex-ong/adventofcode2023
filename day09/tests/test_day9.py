from day09.day9 import INPUT_SMALL, ValueArray, get_input, interpolate, part1, part2


def test_get_input() -> None:
    values: list[ValueArray] = get_input(INPUT_SMALL)
    assert len(values) == 3
    assert len(values[0].sub_arrays) == 3
    assert values[0].sub_arrays[0] == [0, 3, 6, 9, 12, 15]


def test_interpolate() -> None:
    values = [0, 3, 6, 9, 12, 15]
    assert interpolate(values) == [3, 3, 3, 3, 3]


def test_part1() -> None:
    values: list[ValueArray] = get_input(INPUT_SMALL)
    assert part1(values) == 114


def test_part2() -> None:
    values: list[ValueArray] = get_input(INPUT_SMALL)
    assert part2(values) == 2
