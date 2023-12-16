"""
Day5 solution
"""
from dataclasses import dataclass, field
from bisect import bisect_left

INT_MAX = 4294967296


@dataclass
class MappingRange:
    """Simple class for start/end range"""

    start: int
    end: int


@dataclass(order=True)
class Mapping:
    """Simple range based mapping"""

    src_start: int
    src_end: int = field(init=False)
    dest_start: int
    dest_end: int = field(init=False, repr=False)
    size: int

    injected: bool = field(default=False)

    def __post_init__(self):
        self.src_end = self.src_start + self.size
        self.dest_end = self.dest_start + self.size

    def get_mapping(self, src_value: int):
        """Converts from src_value to destination"""
        if self.src_start <= src_value < self.src_end:
            return src_value - self.src_start + self.dest_start

        raise ValueError("Item not within mapping range")

    def get_mappings(self, start, end) -> tuple[MappingRange, int]:
        """
        Returns the chunk from start to end, followed by the remainder
        """
        dest_start = start - self.src_start + self.dest_start
        dest_end_uncapped = end - self.src_start + self.dest_start

        if dest_end_uncapped < self.dest_end:
            remaining = 0
        else:
            remaining = dest_end_uncapped - self.dest_end

        dest_end_capped = min(dest_end_uncapped, self.dest_end)

        return MappingRange(dest_start, dest_end_capped), remaining


class NamedMap:
    """
    a named map with a list of mappings
    you can just use this class to search for a mapping
    """

    name: str
    mappings: list[Mapping]

    def __init__(self, name: str):
        """
        This one is a bit weird; the client should add mappings
        after construction, then call finalize_mappings
        This is to keep the file parsing code simpler.
        """
        self.name = name
        self.mappings = []

    def add_mapping(self, mapping: Mapping):
        """Adds a mapping to our list"""
        self.mappings.append(mapping)

    def finalize_mappings(self):
        """
        * Sorts the mappings
        * Fills in any missing ranges
        * Homogenizes so min_mapping is 0, and max_mapping is INT_MAX
        """
        mappings = self.mappings
        mappings.sort()
        # Find gaps in the mappings and fill them in
        filled_in_mappings = []
        prev_mapping = mappings[0]
        for mapping in mappings[1:]:
            start = prev_mapping.src_end
            end = mapping.src_start
            if start < end:
                injected_mapping = Mapping(start, start, end - start, True)
                filled_in_mappings.append(injected_mapping)
            prev_mapping = mapping

        # inject our mappings. We add them to the end, then sort
        mappings.extend(filled_in_mappings)
        mappings.sort()

        self.mappings = self.extend_mapping_range(mappings)

    def extend_mapping_range(self, mappings: list[Mapping]):
        """Ensure that mappings go from 0 -> INT_MAX"""
        if mappings[0].src_start != 0:
            injected_mapping = Mapping(0, 0, mappings[0].src_start, True)
            mappings.insert(0, injected_mapping)
        if mappings[-1].src_end != INT_MAX:
            start = mappings[-1].src_end
            injected_mapping = Mapping(start, start, INT_MAX - start, True)
            mappings.append(injected_mapping)
        return mappings

    def get_mapping(self, value: int):
        """Uses binary search to grab the correct mapping, then apply it to one value"""
        mapping_idx = bisect_left(self.mappings, value, key=lambda m: m.src_end)
        mapping = self.mappings[mapping_idx]
        return mapping.get_mapping(value)

    def get_mapping_ranges(self, src_mapping_ranges: list[MappingRange]):
        """Given a list of mapping ranges, returns a new list of mapping ranges"""
        result = []
        for src_mapping_range in src_mapping_ranges:
            mappings = self.get_mapping_range(src_mapping_range)
            result.extend(mappings)
        return result

    def get_mapping_range(self, src_mapping_range: MappingRange) -> list[MappingRange]:
        """
        Given a range like 100-200, returns a
        list of lists describing the new mapped range
        """
        # make a quick copy first
        src_start, src_end = src_mapping_range.start, src_mapping_range.end
        result: list[MappingRange] = []

        # find out where the start is
        mapping_start_idx = bisect_left(
            self.mappings, src_start, key=lambda m: m.src_end
        )
        remaining = src_end - src_start

        while remaining != 0:
            mapping_start = self.mappings[mapping_start_idx]
            mapping_range, remaining = mapping_start.get_mappings(src_start, src_end)
            result.append(mapping_range)
            src_start = src_end - remaining  # move src_start upwards over time
            mapping_start_idx += 1  # no need to re-bisect. just go next

        return result

    def __str__(self):
        result = str(self.name) + "\n"
        result += "\n".join(str(mapping) for mapping in self.mappings)
        return result


def process_file(file):
    """processes mappings from file"""
    seeds = None
    maps = []
    named_map = None

    for line in file:
        line = line.strip()
        if line.startswith("seeds"):  # grab the seeds
            seeds = line.split(":")[1].split()
            seeds = [int(seed) for seed in seeds]
        elif line.endswith("map:"):  # start a map segment
            current_map_name = line.split(" map:")[0]
            named_map = NamedMap(current_map_name)
            maps.append(named_map)
        elif len(line.strip()) != 0:  # add a mapping to our named_map
            numbers = [int(item) for item in line.split()]
            dest, src, size = numbers
            mapping = Mapping(src_start=src, dest_start=dest, size=size)
            named_map.add_mapping(mapping)

    # finish setup/optimization
    for named_map in maps:
        named_map.finalize_mappings()

    return seeds, maps


def grab_inputs():
    """parses the source file"""
    with open("input.txt", "r", encoding="utf8") as file:
        return process_file(file)


def get_location(seed: int, maps: list[NamedMap]):
    """given a seed, returns the final location"""
    result = seed
    for named_map in maps:
        result = named_map.get_mapping(result)
    return result


def get_location_ranges(seed_ranges: list[MappingRange], maps: list[NamedMap]):
    """Given a list of MappingRange, returns a list of MappingRange's for the final location"""
    result = seed_ranges[:]
    for named_map in maps:
        result = named_map.get_mapping_ranges(result)
    return result


def seed_to_mapping_ranges(data):
    """
    converts from list of seeds to list of MappingRanges.
    They are in the format [start, size]
    """
    pairs = list(zip(data[::2], data[1::2]))
    result = []
    for pair in pairs:
        start, size = pair
        mapping_range = MappingRange(start, start + size)
        result.append(mapping_range)
    return result


def main():
    """main function, solve all the problems"""
    seeds, maps = grab_inputs()
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
