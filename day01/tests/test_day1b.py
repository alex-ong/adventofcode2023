"""Tests for day01b."""
from day01.day1b import INPUT_SMALL, IndexValue, get_input, part2, process_line


def test_process_line() -> None:
    """Tests ``process_line()`` function."""
    assert process_line("two1nine") == 29
    assert process_line("eightwothree") == 83
    assert process_line("abcone2threexyz") == 13
    assert process_line("xtwone3four") == 24
    assert process_line("4nineeightseven2") == 42
    assert process_line("zoneight234") == 14
    assert process_line("7pqrstsixteen") == 76
    assert process_line("zoneight") == 18


def test_get_input() -> None:
    """Tests ``get_input()`` function."""
    lines: list[str] = get_input(INPUT_SMALL)
    assert len(lines) == 7
    assert lines[0].strip() == "two1nine"


def test_index_value() -> None:
    """Tests ``index_value`` class."""
    index_val: IndexValue = IndexValue(0, "1")
    assert str(index_val) == ("(i:0, v:1)")


def test_part2() -> None:
    """Tests ``part2()`` function."""
    lines: list[str] = get_input(INPUT_SMALL)
    assert part2(lines) == 281
