from day05.lib.classes import Mapping, NamedMap


def grab_inputs(path: str) -> tuple[list[int], list[NamedMap]]:
    """Parses the source file"""
    seeds: list[int]
    maps: list[NamedMap] = []
    named_map: NamedMap

    with open(path, "r", encoding="utf8") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("seeds"):  # grab the seeds
            seeds_str = line.split(":")[1].split()
            seeds = [int(seed) for seed in seeds_str]
        elif line.endswith("map:"):  # start a map segment
            current_map_name = line.split(" map:")[0]
            named_map = NamedMap(current_map_name)
            maps.append(named_map)
        elif len(line.strip()) != 0:  # add a mapping to our named_map
            numbers = [int(item) for item in line.split()]
            dest, src, size = numbers
            mapping = Mapping(src_start=src, dest_start=dest, size=size)
            named_map.add_mapping(mapping)

    for named_map in maps:
        named_map.finalize_mappings()

    return seeds, maps
