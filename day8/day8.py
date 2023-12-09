"""day8 solution"""
from dataclasses import dataclass
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


class WorldMap:
    """world map class"""

    def __init__(self):
        self.mappings = {}

    def add_location(self, location: Location):
        """add location to our mappings"""
        self.mappings[location.name] = location


class Cycle:
    """find a cycle"""

    start_location: str
    start_offset: int
    cycle_length: int
    z_locations: list[int]


@dataclass
class Directions:
    """Simple directions string"""

    steps: str

    def get_step(self, index):
        return self.steps[index % len(self.steps)]


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


def main():
    """main function, solve the things"""
    # q1
    directions, world_map = read_input()
    nodes_visited: int = follow_directions(directions, world_map)
    print(nodes_visited)


if __name__ == "__main__":
    main()
