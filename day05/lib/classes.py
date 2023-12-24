from bisect import bisect_left
from dataclasses import dataclass, field

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

    injected: bool = False

    def __post_init__(self) -> None:
        self.src_end = self.src_start + self.size
        self.dest_end = self.dest_start + self.size

    def get_mapping(self, src_value: int) -> int:
        """Converts from src_value to destination"""
        if self.src_start <= src_value < self.src_end:
            return src_value - self.src_start + self.dest_start

        raise ValueError(f"Item not within mapping range {src_value, self}")

    def get_mappings(self, start: int, end: int) -> tuple[MappingRange, int]:
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

    def add_mapping(self, mapping: Mapping) -> None:
        """Adds a mapping to our list"""
        self.mappings.append(mapping)

    def finalize_mappings(self) -> None:
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

    def extend_mapping_range(self, mappings: list[Mapping]) -> list[Mapping]:
        """Ensure that mappings go from 0 -> INT_MAX"""
        if mappings[0].src_start != 0:
            injected_mapping = Mapping(0, 0, mappings[0].src_start, True)
            mappings.insert(0, injected_mapping)
        if mappings[-1].src_end != INT_MAX:
            start = mappings[-1].src_end
            injected_mapping = Mapping(start, start, INT_MAX - start, True)
            mappings.append(injected_mapping)

        return mappings

    def get_mapping(self, value: int) -> int:
        """Uses binary search to grab the correct mapping, then apply it to one value"""
        mapping_idx = bisect_left(self.mappings, value, key=lambda m: m.src_end - 1)
        mapping = self.mappings[mapping_idx]
        return mapping.get_mapping(value)

    def get_mapping_ranges(
        self, src_mapping_ranges: list[MappingRange]
    ) -> list[MappingRange]:
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

    def __str__(self) -> str:
        result = str(self.name) + "\n"
        result += "\n".join(str(mapping) for mapping in self.mappings)
        return result
