from day01.day1b import INPUT_SMALL, IndexValue, get_input, main, process_line


def test_process_line() -> None:
    assert process_line("two1nine") == 29
    assert process_line("eightwothree") == 83
    assert process_line("abcone2threexyz") == 13
    assert process_line("xtwone3four") == 24
    assert process_line("4nineeightseven2") == 42
    assert process_line("zoneight234") == 14
    assert process_line("7pqrstsixteen") == 76
    assert process_line("zoneight") == 18


def test_get_input() -> None:
    lines: list[str] = get_input(INPUT_SMALL)
    assert len(lines) == 7
    assert lines[0].strip() == "two1nine"


def test_index_value() -> None:
    index_val: IndexValue = IndexValue(0, "1")
    assert str(index_val) == ("(i:0, v:1)")


def test_main() -> None:
    assert main(INPUT_SMALL) == 281
