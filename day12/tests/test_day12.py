"""day12 tests."""
from day12.day12 import INPUT_SMALL, SpringLine, calculate_sum, get_input


def test_calculate_sum() -> None:
    """Test ``calculate_sum()``."""
    spring_lines: list[SpringLine] = get_input(INPUT_SMALL)
    assert calculate_sum(spring_lines) == 21

    spring_lines = [spring_line.unfold() for spring_line in spring_lines]
    assert calculate_sum(spring_lines) == 525152


def test_parser() -> None:
    """Test ``get_input()``."""
    spring_lines: list[SpringLine] = get_input(INPUT_SMALL)
    assert spring_lines[0].items == "???.###"
    assert spring_lines[0].broken_springs == [1, 1, 3]
    assert len(spring_lines) == 6


def test_spring_line() -> None:
    """Test ``SpringLine`` class."""
    spring_line = SpringLine("?###????????", [3, 2, 1])
    assert spring_line.calculate() == 10

    spring_line = SpringLine("???.###", [1, 1, 3])
    unfolded = spring_line.unfold()
    assert unfolded.items == "???.###????.###????.###????.###????.###"
    assert unfolded.broken_springs == [1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3]
