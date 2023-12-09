"""day8 solution"""
from collections import defaultdict
from dataclasses import dataclass, field
import itertools


@dataclass
class Location:
    """
    A location on our map,
    with names of other locations
    """

    name: str
    left: str
    right: str


@dataclass
class LocationStep:
    """
    Location + how many steps to get here
    """

    location: Location
    steps: int


class WorldMap:
    """world map class"""

    def __init__(self):
        self.mappings = {}

    def add_location(self, location: Location):
        """add location to our mappings"""
        self.mappings[location.name] = location


@dataclass
class Directions:
    """Simple directions string"""

    steps: str

    def get_step(self, index):
        return self.steps[index % len(self.steps)]


@dataclass
class Cycle:
    """find a cycle"""

    start_location: Location
    location_steps: list[LocationStep]
    cycle_start: LocationStep

    cycle_start_index: int = field(init=False)
    end_zs: list[int] = field(init=False)

    def __post_init__(self):
        self.cycle_start_index = self.location_steps.index(self.cycle_start)
        end_zs: list[int] = []
        for location_step in self.location_steps:
            if location_step.location.name.endswith("Z"):
                end_zs.append(location_step.steps)
        self.end_zs = end_zs


class LocationStepsLookup:
    def __init__(self):
        self.lookup = defaultdict(list)

    def add(self, location_step: LocationStep):
        self.lookup[location_step.location.name].append(location_step)

    def contains(self, location_step: LocationStep):
        my_list = self.lookup[location_step.location.name]
        return location_step in my_list


def read_input():
    """reads input into directions/world_map"""
    with open("input.txt", "r", encoding="utf8") as file:
        directions = Directions(file.readline().strip())
        world_map = WorldMap()
        for line in file:
            line = line.strip()
            if len(line) == 0:
                continue
            # 0123456789012345
            # GXF = (XQB, GFH)
            name, left, right = line[0:3], line[7:10], line[12:15]
            location = Location(name, left, right)
            world_map.add_location(location)
    return directions, world_map


def follow_directions(directions: Directions, world_map: WorldMap) -> int:
    """follows directions until we hit zzz"""

    mappings = world_map.mappings
    node: Location = mappings["AAA"]
    nodes_visited = 0
    for step in itertools.cycle(directions.steps):
        if step == "L":
            node = mappings[node.left]
        else:  # step == "R":
            node = mappings[node.right]
        nodes_visited += 1
        if node.name == "ZZZ":
            return nodes_visited

    return -1


def follow_directions_multi(directions: Directions, world_map: WorldMap) -> int:
    """Follow all mappings ending in A until all of them are ZZZ"""
    mappings = world_map.mappings
    nodes: list[Location] = [
        location for location in mappings.values() if location.name.endswith("A")
    ]

    cycle1 = find_cycle(nodes[0], world_map, directions)

    print(len(cycle1.location_steps))
    print(cycle1.cycle_start_index)
    print(cycle1.end_zs)
    return 0


def find_cycle(location: Location, world_map: WorldMap, directions: Directions):
    start_location = location
    nodes: list[LocationStep] = []
    step_count = 0
    mappings = world_map.mappings

    node = LocationStep(location, step_count)
    location_steps_lookup = LocationStepsLookup()

    while True:
        nodes.append(node)
        location_steps_lookup.add(node)

        direction = directions.steps[step_count]
        if direction == "L":
            location = mappings[location.left]
        else:
            location = mappings[location.right]

        node = LocationStep(location, step_count + 1)
        if location_steps_lookup.contains(node):
            break

        step_count += 1
        step_count %= len(directions.steps)

    return Cycle(start_location, nodes, node)


def main():
    """main function, solve the things"""
    # q1
    directions, world_map = read_input()
    nodes_visited: int = follow_directions(directions, world_map)
    print(nodes_visited)
    follow_directions_multi(directions, world_map)


if __name__ == "__main__":
    main()
