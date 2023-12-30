"""Test main functions for day17."""
from day17.day17 import INPUT_PT2, INPUT_SMALL, part1, part2
from day17.lib.parsers import get_input


def test_parts() -> None:
    """Test ``part1()`` and ``part2``."""
    input: list[list[int]] = get_input(INPUT_SMALL)
    assert part1(input) == 102
    assert part2(input) == 94

    input_pt2: list[list[int]] = get_input(INPUT_PT2)
    assert part2(input_pt2) == 71
