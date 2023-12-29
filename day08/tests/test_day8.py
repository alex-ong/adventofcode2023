"""day08 tests."""
from day08.day8 import (
    INPUT_A,
    INPUT_B,
    INPUT_C,
    Cycle,
    Directions,
    Location,
    find_cycle,
    follow_directions,
    follow_directions_multi,
    get_location_as,
    read_input,
)


def test_part1() -> None:
    """Test ``part1()``."""
    directions, world_map = read_input(INPUT_A)
    assert follow_directions(directions, world_map) == 2

    directions, world_map = read_input(INPUT_B)
    assert follow_directions(directions, world_map) == 6


def test_part2() -> None:
    """Test ``part2()``."""
    directions, world_map = read_input(INPUT_C)
    assert follow_directions_multi(directions, world_map) == 6


def test_location_as() -> None:
    """Test finding of the ``a`` locations."""
    _, world_map = read_input(INPUT_C)
    locations: list[Location] = get_location_as(world_map)
    names = [location.name for location in locations]
    assert set(names) == {"11A", "22A"}


def test_find_cycle() -> None:
    """Test finding cycles."""
    directions, world_map = read_input(INPUT_C)
    locations: list[Location] = get_location_as(world_map)

    location_11A: Location = [loc for loc in locations if loc.name == "11A"][0]
    location_22A: Location = [loc for loc in locations if loc.name == "22A"][0]

    cycle_11A: Cycle = find_cycle(location_11A, world_map, directions)
    cycle_22A: Cycle = find_cycle(location_22A, world_map, directions)
    assert cycle_11A.cycle_length == 2
    assert cycle_22A.cycle_length == 6


def test_directions() -> None:
    """Test directions class."""
    directions: Directions = Directions("LRLRLLR")
    assert directions.get_step(0) == "L"
    assert directions.get_step(7) == "L"
