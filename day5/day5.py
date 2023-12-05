from dataclasses import dataclass, field


@dataclass
class Mapping:
    """Simple range based mapping"""

    src_start: int
    src_end: int = field(init=False)
    dest_start: int
    size: int

    def __post_init__(self):
        self.src_end = self.src_start + self.size

    def get_mapping(self, value: int):
        """Return None if value not in mapping"""
        if self.src_start <= value <= self.src_end:
            return value - self.src_start + self.dest_start
        return None


class Map:
    """
    a named map with a list of mappings
    you can just use this class to search for a mapping
    """

    def __init__(self, name, mappings):
        self.name: str = name
        self.mappings = self.finalize_mappings(mappings)
        self.min_mapping = self.mappings[0].src_start
        self.max_mapping = self.mappings[-1].src_start + self.mappings[-1].size

    def finalize_mappings(self, mappings: list[Mapping]):
        """sorts the mappings"""
        mappings.sort(key=lambda m: m.src_start)
        return mappings
        """
        filled_in_mappings = []
        # fill in the mappings
        prev_mapping = mappings[0]
        for mapping in mappings[1:]:
            start = prev_mapping.src_end + 1
            end = mapping.src_start
            if start < end:
                mapping = Mapping(start, start, end - start)
                filled_in_mappings.append(mapping)
            prev_mapping = mapping
        mappings.extend(filled_in_mappings)
        mappings.sort(key=lambda m: m.src_start)
        return mappings
        """

    def get_mapping(self, value: int):
        for mapping in self.mappings:
            result = mapping.get_mapping(value)
            if result is not None:
                return result
        return value

    def get_mapping_range(self, start_range: int, end_range: int):
        """given a range like 100-200, returns a
        list of lists describing the new mapped range"""

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
    print("Evalulating", seed)
    result = seed
    for map in maps:
        result = map.get_mapping(result)
        print(map.name, result)
    return result


def main():
    seeds, maps = grab_inputs()
    locations = [get_location(seed, maps) for seed in seeds]
    locations.sort()
    print(locations[0])


if __name__ == "__main__":
    main()
