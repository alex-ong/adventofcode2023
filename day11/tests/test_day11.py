from day11.day11 import INPUT_SMALL, Universe, get_total_distance, is_empty, parse_input


def test_day11() -> None:
    universe: Universe = parse_input(INPUT_SMALL)
    assert universe.num_rows == 10
    assert universe.num_cols == 10
    universe.expand_contents()
    galaxies = universe.grab_galaxies()

    # q1: expansion = 2
    assert galaxies[0].distance(galaxies[6], universe) == 15
    assert galaxies[2].distance(galaxies[5], universe) == 17
    assert galaxies[7].distance(galaxies[8], universe) == 5

    assert get_total_distance(galaxies, universe) == 374
    # q2: expansion = 1000000
    universe.expansion_rate = 10
    assert get_total_distance(galaxies, universe) == 1030
    universe.expansion_rate = 100
    assert get_total_distance(galaxies, universe) == 8410


def test_is_empty() -> None:
    universe: Universe = parse_input(INPUT_SMALL)
    assert is_empty(universe.contents[3])
    assert not is_empty(universe.contents[0])
    assert not is_empty(universe.contents[1])
    assert not is_empty(universe.contents[2])