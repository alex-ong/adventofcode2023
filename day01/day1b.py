"""day1b solution."""


from dataclasses import dataclass

INPUT = "day01/input.txt"
INPUT_SMALL = "day01/input-small2.txt"


@dataclass
class IndexValue:
    """index to value mapping."""

    index: int = 0
    value: str = "1"

    def __str__(self) -> str:
        """to_string function.

        Returns:
            str: ``(i:{index}, v:{value})``
        """
        return f"(i:{self.index}, v:{self.value})"


@dataclass
class WordNumber:
    """Simple mapping from word to integer."""

    word: str = "one"
    number: str = "1"


MAPPINGS: list[WordNumber] = [
    WordNumber("one", "1"),
    WordNumber("two", "2"),
    WordNumber("three", "3"),
    WordNumber("four", "4"),
    WordNumber("five", "5"),
    WordNumber("six", "6"),
    WordNumber("seven", "7"),
    WordNumber("eight", "8"),
    WordNumber("nine", "9"),
]


def process_line(line: str) -> int:
    """Processes a line, returning the first and last integer.

    Substrings like ``nine`` and ``one`` count as integers,
    as do ``1`` and ``9``.

    Args:
        line (str): a line to process

    Returns:
        int: integer value of the two numbers concatenated
    """
    index_to_chars = {}
    for index, char in enumerate(line):
        if char.isnumeric():
            index_to_chars[index] = char

        for mapping in MAPPINGS:
            substring = line[index : index + len(mapping.word)]
            if substring == mapping.word:
                index_to_chars[index] = mapping.number

    print(index_to_chars, line)
    first_index = min(index_to_chars.keys())
    last_index = max(index_to_chars.keys())

    return int(index_to_chars[first_index] + index_to_chars[last_index])


def get_input(input_file: str) -> list[str]:
    """Opens a file and returns a list of strings to handle.

    Args:
        input_file (str): filepath of input

    Returns:
        list[str]: list of strings to parse
    """
    with open(input_file, "r", encoding="utf8") as file:
        return list(file)


def part2(lines: list[str]) -> int:
    """Returns sum of "first/last" numbers in line.

    Args:
        lines (list[str]): list of lines to handle

    Returns:
        int: sum of "first/last" numbers in line
    """
    total = sum(process_line(line) for line in lines)
    return total


def main() -> None:
    """Grabs input and then processes it."""
    lines = get_input(INPUT)
    print(part2(lines))


if __name__ == "__main__":
    main()
