"""day1a solution"""


from typing import Optional

INPUT = "day01/input.txt"
INPUT_SMALL = "day01/input-small.txt"


def get_first_last(line: str) -> tuple[str, str]:
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
    with open(input_file, "r", encoding="utf8") as file:
        return list(file)


def part1(lines: list[str]) -> int:
    total = 0
    for line in lines:
        first, last = get_first_last(line)
        data = int(first + last)
        total += data
    return total


def main() -> None:
    lines = get_input(INPUT)
    print(part1(lines))


if __name__ == "__main__":
    main()
