from typing import TYPE_CHECKING

from day05.day5 import INPUT_SMALL, part1, part2, seed_to_mapping_ranges
from day05.lib.classes import MappingRange
from day05.lib.parsers import grab_inputs

if TYPE_CHECKING:
    from day05.lib.classes import NamedMap


def test_mapping() -> None:
    seeds: list[int]
    maps: list[NamedMap]
    seeds, maps = grab_inputs(INPUT_SMALL)

    assert len(seeds) == 4
    assert len(maps) == 7

    results = [79, 81, 81, 81, 74, 78, 78, 82]

    for index, map in enumerate(maps):
        assert map.get_mapping(results[index]) == results[index + 1]


def test_part1() -> None:
    seeds, maps = grab_inputs(INPUT_SMALL)
    assert part1(seeds, maps) == 35


def test_part2() -> None:
    seeds, maps = grab_inputs(INPUT_SMALL)
    assert part2(seeds, maps) == 46


def test_seed_to_mapping_ranges() -> None:
    data = [79, 14, 55, 13]
    # 79, len(14) -> 79, 93
    # 55, len(13) -> 55, 68
    ranges = seed_to_mapping_ranges(data)
    assert ranges[0] == MappingRange(79, 93)
    assert ranges[1] == MappingRange(55, 68)
