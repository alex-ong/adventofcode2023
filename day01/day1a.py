"""day1a solution"""


from typing import Optional


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


def main() -> None:
    with open("day01/input.txt", "r", encoding="utf8") as file:
        total = 0
        for line in file:
            first, last = get_first_last(line)
            data = int(first + last)
            total += data
        print(total)


if __name__ == "__main__":
    main()
