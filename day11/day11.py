"""day11 solution"""
from dataclasses import dataclass, field
from typing import Iterator

INPUT = "day11/input.txt"
INPUT_SMALL = "day11/input-small.txt"


@dataclass
class Galaxy:
    """Galaxy represented as its position and unique id"""

    row: int
    col: int
    id: int

    def distance(self, other: "Galaxy", universe: "Universe") -> int:
        start_row, end_row = sorted([self.row, other.row])
        start_col, end_col = sorted([self.col, other.col])
        result = 0
        expansion_rate = universe.expansion_rate

        for row in range(start_row, end_row):
            result += universe[row][start_col].get_point_distance(expansion_rate)
        for col in range(start_col, end_col):
            result += universe[end_row][col].get_point_distance(expansion_rate)
        return result


@dataclass
class Point:
    """Point represented by character and whether it is expanded"""

    row: int
    col: int
    item: str
    is_expanded: bool = field(default=False, init=False)

    def get_point_distance(self, expansion_rate: int) -> int:
        """Returns how big this "point" is based on if its expanded"""
        if self.is_expanded:
            return expansion_rate
        return 1

    def __str__(self) -> str:
        if self.is_expanded:
            return "@"
        return self.item


@dataclass
class Universe:
    """Universe class; 2d array of . and #"""

    contents: list[list[Point]]
    expansion_rate: int = 2

    num_rows: int = field(repr=False, init=False)
    num_cols: int = field(repr=False, init=False)

    def __post_init__(self) -> None:
        self.num_rows = len(self.contents)
        self.num_cols = len(self.contents[0])

    def __getitem__(self, row_index: int) -> list[Point]:
        """
        we can just use universe[row]
        instead of universe.contents[row]
        """
        return self.contents[row_index]

    def __iter__(self) -> Iterator[list[Point]]:
        """
        we can just use `for row in universe`
        instead of `for row in universe.contents`
        """
        for row in self.contents:
            yield row

    def expand_contents(self) -> None:
        """expands the contents of the universe"""
        for row in self.contents:
            if is_empty(row):
                for item in row:
                    item.is_expanded = True

        col_index = 0
        while col_index < len(self.contents[0]):
            col = [row[col_index] for row in self.contents]
            if is_empty(col):
                for item in col:
                    item.is_expanded = True
            col_index += 1

    def grab_galaxies(self) -> list[Galaxy]:
        """grabs all galaxies"""
        results = []
        galaxy_id = 0
        for index_row, row in enumerate(self.contents):
            for index_col, col in enumerate(row):
                if col.item == "#":
                    results.append(Galaxy(index_row, index_col, galaxy_id))
                    galaxy_id += 1
        return results

    def __str__(self) -> str:
        return "\n".join("".join(str(col) for col in row) for row in self.contents)


def is_empty(items: list[Point]) -> bool:
    """returns True if all the content is "." """
    has_content = any(x.item == "#" for x in items)
    return not has_content


def parse_input(path: str) -> Universe:
    """parse input file and return a universe"""
    with open(path, "r", encoding="utf8") as file:
        rows = []
        for row, line in enumerate(file):
            line = line.strip()
            row_points = [Point(row, col, item) for col, item in enumerate(line)]
            rows.append(row_points)
        return Universe(rows)


def get_total_distance(galaxies: list[Galaxy], universe: Universe) -> int:
    """returns total distance of all galaxies"""
    result = 0
    for index, galaxy in enumerate(galaxies):
        for galaxy2 in galaxies[index + 1 :]:
            distance = galaxy.distance(galaxy2, universe)
            result += distance
    return result


def main() -> None:
    """main function, runs q1 and q2"""
    universe: Universe = parse_input(INPUT)
    universe.expand_contents()
    galaxies = universe.grab_galaxies()

    # q1: expansion = 2
    print(get_total_distance(galaxies, universe))
    # q2: expansion = 1000000
    universe.expansion_rate = 1000000
    print(get_total_distance(galaxies, universe))


if __name__ == "__main__":
    main()
