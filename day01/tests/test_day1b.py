from day01.day1b import process_line


def test_process_line() -> None:
    assert process_line("two1nine") == 29
    assert process_line("eightwothree") == 83
    assert process_line("abcone2threexyz") == 13
    assert process_line("xtwone3four") == 24
    assert process_line("4nineeightseven2") == 42
    assert process_line("zoneight234") == 14
    assert process_line("7pqrstsixteen") == 76
    assert process_line("zoneight") == 18
