"""Day5 mainfile tests."""
from typing import TYPE_CHECKING

import pytest

from day05.day5 import INPUT_GAPS, INPUT_SMALL, part1, part2, seed_to_mapping_ranges
from day05.lib.classes import Mapping, MappingRange
from day05.lib.parsers import grab_inputs

if TYPE_CHECKING:
    from day05.lib.classes import NamedMap


def test_mapping() -> None:
    """Test ``NamedMap`` class."""
    seeds: list[int]
    maps: list[NamedMap]
    seeds, maps = grab_inputs(INPUT_SMALL)

    assert len(seeds) == 4
    assert len(maps) == 7

    results = [79, 81, 81, 81, 74, 78, 78, 82]

    for index, map in enumerate(maps):
        assert map.get_mapping(results[index]) == results[index + 1]

    # call mapping with integer outside its range
    mapping: Mapping = maps[0].mappings[0]
    with pytest.raises(ValueError):
        mapping.get_mapping(mapping.src_end + 1)

    seeds, maps = grab_inputs(INPUT_GAPS)

    assert str(maps[0]) == "\n".join(
        [
            "seed-to-soil",
            "Mapping(src_start=0, src_end=15, dest_start=0, size=15, injected=True)",
            "Mapping(src_start=15, src_end=63, dest_start=15, size=48, injected=False)",
            "Mapping(src_start=63, src_end=100, dest_start=63, size=37, injected=True)",
            "Mapping(src_start=100, src_end=120, dest_start=100, size=20, injected=False)",
            "Mapping(src_start=120, src_end=4294967290, dest_start=120, size=4294967170, injected=True)",
            "Mapping(src_start=4294967290, src_end=4294967296, dest_start=4294967290, size=6, injected=False)",
        ]
    )


def test_part1() -> None:
    """Test ``part1()``."""
    seeds, maps = grab_inputs(INPUT_SMALL)
    assert part1(seeds, maps) == 35


def test_part2() -> None:
    """Test ``part2()``."""
    seeds, maps = grab_inputs(INPUT_SMALL)
    assert part2(seeds, maps) == 46


def test_seed_to_mapping_ranges() -> None:
    """Test construction of mapping ranges for part2."""
    data = [79, 14, 55, 13]
    # 79, len(14) -> 79, 93
    # 55, len(13) -> 55, 68
    ranges = seed_to_mapping_ranges(data)
    assert ranges[0] == MappingRange(79, 93)
    assert ranges[1] == MappingRange(55, 68)
