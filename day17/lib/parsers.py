"""parse input file"""


def get_input(path: str) -> list[list[int]]:
    """Convert input into world dataclass"""
    with open(path, "r", encoding="utf8") as file:
        data: list[list[int]] = []
        for line in file:
            data.append([int(char) for char in line.strip()])
        return data
