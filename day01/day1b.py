"""day1b solution"""


from dataclasses import dataclass


@dataclass
class IndexValue:
    """index to value mapping"""

    index: int = 0
    value: str = "1"

    def __str__(self) -> str:
        return f"(i:{self.index}, v:{self.value})"


@dataclass
class WordNumber:
    word: str = "one"
    number: str = "1"


mappings = [
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
    index_to_chars = {}
    for index, char in enumerate(line):
        if char.isnumeric():
            index_to_chars[index] = char

        for mapping in mappings:
            substring = line[index : index + len(mapping.word)]
            if substring == mapping.word:
                index_to_chars[index] = mapping.number

    print(index_to_chars, line)
    first_index = min(index_to_chars.keys())
    last_index = max(index_to_chars.keys())

    return int(index_to_chars[first_index] + index_to_chars[last_index])


def main() -> None:
    with open("input.txt", "r", encoding="utf8") as file:
        total = 0
        for line in file:
            total += process_line(line)

        print(total)


if __name__ == "__main__":
    main()
