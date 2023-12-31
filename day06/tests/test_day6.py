"""tests for day06."""
from day06.day6 import (
    INPUT_SMALL,
    Race,
    calculate_constant_time,
    calculate_race,
    get_giga_race,
    part1,
    part2,
    read_inputs,
)


def test_read_inputs() -> None:
    """Tests reading inputs from file."""
    races: list[Race] = read_inputs(INPUT_SMALL)
    assert races[0] == Race(7, 9)
    assert races[1] == Race(15, 40)
    assert races[2] == Race(30, 200)


def test_get_giga_race() -> None:
    """Tests reading the input for the giga race."""
    races: list[Race] = read_inputs(INPUT_SMALL)
    race = get_giga_race(races)
    assert race == Race(71530, 940200)


def test_part1() -> None:
    """Tests part1."""
    races: list[Race] = read_inputs(INPUT_SMALL)
    assert part1(races) == 288


def test_part2() -> None:
    """Tests part2."""
    races: list[Race] = read_inputs(INPUT_SMALL)
    race = get_giga_race(races)
    assert part2(race) == 71503


def test_calculate_race() -> None:
    """Tests calculating the race in both constant-time and brute-force."""
    race = Race(7, 9)
    assert calculate_race(race) == 4
    assert calculate_constant_time(race) == 4


def test_calculate_constant_time() -> None:
    """Test calculating constant time."""
    assert calculate_constant_time(Race(7, 9)) == 4

    assert calculate_constant_time(Race(71530, 940200)) == 71503
