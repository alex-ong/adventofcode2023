"""Test day19 main classes."""
from day19.day19 import INPUT_SMALL, get_input, part1, part2


def test_day19() -> None:
    """Test ``part1()`` and ``part2()``."""
    workflows, parts = get_input(INPUT_SMALL)

    assert part1(workflows, parts) == 19114
    assert part2(workflows) == 167409079868000
