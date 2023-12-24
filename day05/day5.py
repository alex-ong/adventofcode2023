"""
Day5 solution
"""

from day05.lib.classes import MappingRange, NamedMap
from day05.lib.parsers import grab_inputs

INPUT = "day05/input.txt"
INPUT_SMALL = "day05/input-small.txt"


def get_location(seed: int, maps: list[NamedMap]) -> int:
    """given a seed, returns the final location"""
    result = seed
    for named_map in maps:
        result = named_map.get_mapping(result)
    return result


def get_location_ranges(
    seed_ranges: list[MappingRange], maps: list[NamedMap]
) -> list[MappingRange]:
    """Given a list of MappingRange, returns a list of MappingRange's for the final location"""
    result = seed_ranges[:]
    for named_map in maps:
        result = named_map.get_mapping_ranges(result)
    return result


def seed_to_mapping_ranges(data: list[int]) -> list[MappingRange]:
    """
    converts from list of seeds to list of MappingRanges.
    They are in the format [start, size]
    """
    pairs = list(zip(data[::2], data[1::2]))
    result: list[MappingRange] = []
    for pair in pairs:
        start, size = pair
        mapping_range = MappingRange(start, start + size)
        result.append(mapping_range)
    return result


def main() -> None:
    """main function, solve all the problems"""
    seeds, maps = grab_inputs(INPUT)
    # q1
    locations = [get_location(seed, maps) for seed in seeds]
    locations.sort()
    print(locations[0])

    # q2
    start_ranges = seed_to_mapping_ranges(seeds)
    end_locations = get_location_ranges(start_ranges, maps)
    print(min(location.start for location in end_locations))


if __name__ == "__main__":
    main()
