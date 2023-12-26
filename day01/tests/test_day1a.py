import pytest

from day01.day1a import INPUT_SMALL, get_first_last, get_input, main


def test_get_first_last() -> None:
    assert get_first_last("abcdef123asdf4") == ("1", "4")
    assert get_first_last("1") == ("1", "1")
    assert get_first_last("01") == ("0", "1")

    assert get_first_last("1abc2") == ("1", "2")
    assert get_first_last("pqr3stu8vwx") == ("3", "8")
    assert get_first_last("a1b2c3d4e5f") == ("1", "5")
    assert get_first_last("treb7uchet") == ("7", "7")

    with pytest.raises(ValueError):
        get_first_last("")


def test_main() -> None:
    assert main(INPUT_SMALL) == 142


def test_get_input() -> None:
    lines: list[str] = get_input(INPUT_SMALL)
    assert len(lines) == 4
    assert lines[0].strip() == "1abc2"
