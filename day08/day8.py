"""day8 solution"""
from dataclasses import dataclass, field
import math
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

    def __hash__(self):
        return hash(self.location.name + str(self.steps))


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
    location_steps: list[LocationStep]  # all the steps, including non-looping
    cycle_start: LocationStep  # the step that loops

    cycle_start_index: int = field(init=False)  # index of cycle_start
    end_zs: list[int] = field(init=False)

    @property
    def cycle_length(self):
        """return length of the repeating part"""
        return len(self.location_steps) - self.cycle_start_index

    def __post_init__(self):
        self.cycle_start_index = self.location_steps.index(self.cycle_start)
        end_zs: list[int] = []
        for index, location_step in enumerate(self.location_steps):
            if location_step.location.name.endswith("Z"):
                end_zs.append(index)
        self.end_zs = end_zs

    def get_location(self, index):
        if index < len(self.location_steps):
            return self.location_steps[index]

        # 2nd half of array is from cycle_start_index -> end
        index -= len(self.location_steps)
        index %= self.cycle_length
        index += self.cycle_start_index
        if index >= len(self.location_steps):
            raise ValueError("you fucked up")
        return self.location_steps[index]


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
        else:
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

    cycles = [find_cycle(node, world_map, directions) for node in nodes]

    for cycle in cycles:
        print(
            cycle.start_location,
            cycle.cycle_start_index,
            len(cycle.location_steps),
            cycle.cycle_length,
            cycle.end_zs,
        )

    # each cycle only has one z in it.
    # Also, each path is
    # [beginning][loop------z--endloop]
    # endloop.size == beginning.size

    # That means it can be simplified by finding the lcm

    lcm = math.lcm(*[cycle.cycle_length for cycle in cycles])
    print(lcm)  # 13,663,968,099,527

    index = cycles[0].end_zs[0]
    index = lcm
    for cycle in cycles:
        print(cycle.get_location(index))

    return lcm


def find_cycle(location: Location, world_map: WorldMap, directions: Directions):
    start_location = location
    nodes: list[LocationStep] = []
    step_count = 0
    mappings = world_map.mappings

    node = LocationStep(location, step_count)
    location_steps_lookup = set()

    while True:
        nodes.append(node)
        location_steps_lookup.add(node)

        direction = directions.steps[step_count]
        if direction == "L":
            location = mappings[location.left]
        else:
            location = mappings[location.right]

        node = LocationStep(location, step_count + 1)
        if node in location_steps_lookup:
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