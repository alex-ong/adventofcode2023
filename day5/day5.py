"""
Day5 solution
"""
from dataclasses import dataclass, field
from bisect import bisect_left

INT_MAX = 4294967296


@dataclass
class MappingRange:
    start: int
    end: int


@dataclass
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

    def check_mapping(self, value: int):
        """Comparitor function to check if a value is within our range"""
        if value < self.src_start:
            return -1
        if value >= self.src_end:
            return 1
        return 0

    def get_mapping(self, value: int):
        """Return None if value not in mapping"""
        if self.src_start <= value < self.src_end:
            return value - self.src_start + self.dest_start

        raise ValueError("item not within mapping range")

    def get_mappings(self, start, end) -> tuple[MappingRange, int]:
        """
        Returns the chunk from start to end, followed by the remainder
        """
        left = start - self.src_start + self.dest_start
        right_uncapped = end - self.src_start + self.dest_start

        if right_uncapped < self.dest_end:
            remaining = 0
        else:
            remaining = right_uncapped - self.dest_end

        right_capped = min(right_uncapped, self.dest_end)

        return MappingRange(left, right_capped), remaining


class Map:
    """
    a named map with a list of mappings
    you can just use this class to search for a mapping
    """

    name: str
    mappings: list[Mapping]
    min_mapping: int
    max_mapping: int

    def __init__(self, name: str, mappings):
        self.name = name
        self.mappings = self.finalize_mappings(mappings)
        self.min_mapping = self.mappings[0].src_start
        self.max_mapping = self.mappings[-1].src_end

    def finalize_mappings(self, mappings: list[Mapping]):
        """
        sorts the mappings
        Fills in any missing ranges
        Homogenizes so min_mapping is 0, and max_mapping is INT_MAX
        """
        mappings.sort(key=lambda m: m.src_start)

        filled_in_mappings = []
        # fill in the mappings
        prev_mapping = mappings[0]

        for mapping in mappings[1:]:
            start = prev_mapping.src_end
            end = mapping.src_start
            if start < end:
                injected_mapping = Mapping(start, start, end - start, True)
                filled_in_mappings.append(injected_mapping)
            prev_mapping = mapping
        mappings.extend(filled_in_mappings)
        mappings.sort(key=lambda m: m.src_start)

        # inject start and end mappings:
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
        result = []
        for src_mapping_range in src_mapping_ranges:
            mappings = self.get_mapping_range(src_mapping_range)
            result.extend(mappings)
        return result

    def get_mapping_range(self, src_mapping_range: MappingRange) -> list[MappingRange]:
        """given a range like 100-200, returns a
        list of lists describing the new mapped range"""
        # make a quick copy first
        src_start, src_end = src_mapping_range.start, src_mapping_range.end

        mapping_start_idx = bisect_left(
            self.mappings, src_start, key=lambda m: m.src_end
        )

        result: list[MappingRange] = []
        mapping_start: Mapping = self.mappings[mapping_start_idx]
        mapping_range, remaining = mapping_start.get_mappings(src_start, src_end)
        result.append(mapping_range)

        while remaining != 0:
            src_start = src_end - remaining
            mapping_start_idx += 1
            mapping_start = self.mappings[mapping_start_idx]
            mapping_range, remaining = mapping_start.get_mappings(src_start, src_end)
            result.append(mapping_range)

        return result

    def __str__(self):
        result = str(self.name) + "\n"
        result += "\n".join(str(mapping) for mapping in self.mappings)
        return result


def process_file(file):
    """processes mappings from file"""
    seeds = None
    maps = []
    current_map_name = None
    current_mappings = []

    for line in file:
        line = line.strip()
        if line.startswith("seeds"):
            seeds = line.split(":")[1].split()
            seeds = [int(seed) for seed in seeds]
        elif line.endswith("map:"):
            current_map_name = line.split()
            current_map_name = line.split(" map:")[0]
            current_mappings = []
        elif len(line) == 0:
            if current_map_name is not None and len(current_mappings) > 0:
                map = Map(name=current_map_name, mappings=current_mappings)
                maps.append(map)
                current_map_name = None
        else:
            numbers = [int(item) for item in line.split()]
            dest, src, size = numbers
            mapping = Mapping(src_start=src, dest_start=dest, size=size)
            current_mappings.append(mapping)

    # there is no newline at end of file, so add the last mapping
    if current_map_name is not None and len(current_mappings) > 0:
        map = Map(name=current_map_name, mappings=current_mappings)
        maps.append(map)
    return seeds, maps


def grab_inputs():
    """parses the source file"""
    with open("input.txt", "r", encoding="utf8") as file:
        return process_file(file)


def get_location(seed, maps: list[Map]):
    result = seed
    for map in maps:
        result = map.get_mapping(result)
    return result


def get_location_ranges(seed_ranges: list[MappingRange], maps: list[Map]):
    result = seed_ranges[:]
    for map in maps:
        result = map.get_mapping_ranges(result)
    return result


def seed_to_mapping_ranges(data):
    pairs = list(zip(data[::2], data[1::2]))
    result = []
    for pair in pairs:
        start, size = pair
        mapping_range = MappingRange(start, start + size)
        result.append(mapping_range)
    return result


def main():
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
