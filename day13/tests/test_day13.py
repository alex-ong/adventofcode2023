"""Day13 tests."""
from day13.day13 import INPUT_SMALL, Maze, distance, read_input


def test_day13() -> None:
    """Test day13."""
    mazes: list[Maze] = read_input(INPUT_SMALL)
    assert len(mazes) == 2
    assert mazes[0].solve() == 5
    assert mazes[1].solve() == 400

    assert mazes[0].solve(1) == 300
    assert mazes[1].solve(1) == 100


def test_distance() -> None:
    """Test ``distance()`` function."""
    str1 = "#...##..#"
    str2 = "##..##..#"
    str3 = "######..#"

    assert distance(str1, str2) == 1
    assert distance(str1, str3) == 3
