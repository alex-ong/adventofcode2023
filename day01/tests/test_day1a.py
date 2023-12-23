from day01.day1a import get_first_last


def test_get_first_last() -> None:
    assert get_first_last("abcdef123asdf4") == ("1", "4")
    assert get_first_last("1") == ("1", "1")
    assert get_first_last("01") == ("0", "1")

    assert get_first_last("1abc2") == ("1", "2")
    assert get_first_last("pqr3stu8vwx") == ("3", "8")
    assert get_first_last("a1b2c3d4e5f") == ("1", "5")
    assert get_first_last("treb7uchet") == ("7", "7")
