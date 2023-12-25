from typing import TYPE_CHECKING

from day16.day16 import INPUT_SMALL, part1, part2
from day16.lib.parsers import get_input

if TYPE_CHECKING:
    from day16.lib.world import World


def test_part1() -> None:
    world: World = get_input(INPUT_SMALL)
    assert part1(world) == 46


def test_part2() -> None:
    world: World = get_input(INPUT_SMALL)
    assert part2(world) == 51
