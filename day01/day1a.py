"""
day1a solution
"""


from typing import Optional

INPUT = "day01/input.txt"
INPUT_SMALL = "day01/input-small.txt"


def get_first_last(line: str) -> tuple[str, str]:
    """
    Returns first and last numeric character of a string
    It can be the same character

    Args:
        line (str): string to parse

    Raises:
        ValueError: When there are no numbers in the string

    Returns:
        tuple[str, str]: first char, last char
    """
    first: Optional[str] = None
    last: str
    for char in line:
        if char.isnumeric():
            if first is None:
                first = char
            last = char

    if first is None:
        raise ValueError("first should be set by now")
    return (first, last)


def get_input(input_file: str) -> list[str]:
    """
    Grabs list of lines to parse from input file

    Args:
        input_file (str): input file's name

    Returns:
        list[str]: list of lines to parse
    """

    with open(input_file, "r", encoding="utf8") as file:
        return list(file)


def part1(lines: list[str]) -> int:
    """
    Runs day1/part1 of adventofcode2023

    Args:
        lines (list[str]): list of lines to parse

    Returns:
        int: sum of results for each line.
    """
    total = 0
    for line in lines:
        first, last = get_first_last(line)
        data = int(first + last)
        total += data
    return total


def main() -> None:
    """Grabs input then processes it"""
    lines = get_input(INPUT)
    print(part1(lines))


if __name__ == "__main__":
    main()
