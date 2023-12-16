"""day13 solution"""

from dataclasses import dataclass, field
import itertools
from math import floor, ceil


@dataclass
class Maze:
    tiles: list[str]

    row_reflect: float | None = field(init=False, default=None)
    col_reflect: float | None = field(init=False, default=None)

    @property
    def num_cols(self):
        return len(self.tiles[0])

    @property
    def num_rows(self):
        return len(self.tiles)

    def __post_init__(self):
        """post setup"""
        self.reflect_rows()
        self.reflect_cols()

    def __str__(self):
        if self.col_reflect is not None:
            result = self.col_number_header() + self.col_arrow_header()
            result += "\n".join(str(tile) for tile in self.tiles) + "\n"
            result += self.col_arrow_header() + self.col_number_header()
            result += f"col: {self.col_reflect+1}"
        elif self.row_reflect is not None:
            result = ""
            numbers = self.get_numbers(self.num_rows)
            for index, line in enumerate(self.tiles):
                pointer = " "
                if index == floor(self.row_reflect):
                    pointer = "v"
                elif index == ceil(self.row_reflect):
                    pointer = "^"
                result += (
                    numbers[index]
                    + pointer
                    + str(line)
                    + " "
                    + pointer
                    + numbers[index]
                    + "\n"
                )
            result += f"row: {self.row_reflect+1}"
        return result

    def get_numbers(self, max_number):
        return "".join(itertools.islice(itertools.cycle("1234567890"), max_number))

    def col_number_header(self):
        if self.col_reflect is not None:
            return self.get_numbers(self.num_cols) + "\n"
        return ""

    def col_arrow_header(self):
        if self.col_reflect is not None:
            return " " * floor(self.col_reflect) + "><" + "\n"
        return ""

    def reflect_rows(self):
        self.row_reflect = self.check_reflection(self.tiles)

    def reflect_cols(self):
        """checks reflection of cols by flipping rows/cols"""
        cols: list[list[str]] = [[] for _ in range(len(self.tiles[0]))]
        for row in self.tiles:
            for col_index, col in enumerate(row):
                cols[col_index].append(col)

        cols_strs = ["".join(str(col)) for col in cols]
        self.col_reflect = self.check_reflection(cols_strs)

    def check_reflection(self, data: list[str]):
        """Checks a reflection on rows or cols"""
        mirror_candidates = []
        for index, row in enumerate(data):
            if index == len(data) - 1:
                break
            if row == data[index + 1]:
                mirror_candidates.append(index + 0.5)

        if len(mirror_candidates) == 0:
            return None

        for mirror_candidate in mirror_candidates:
            works = True
            low_index, high_index = floor(mirror_candidate), ceil(mirror_candidate)
            while low_index >= 0 and high_index < len(data):
                if data[low_index] != data[high_index]:
                    works = False
                    break
                low_index -= 1
                high_index += 1
            if works:
                return mirror_candidate

        return None

    def score(self):
        """returns score for q1"""
        if self.col_reflect is not None:
            return floor(self.col_reflect + 1)
        elif self.row_reflect is not None:
            return 100 * floor(self.row_reflect + 1)
        return 0


def read_input() -> list[Maze]:
    mazes: list[Maze] = []
    with open("input.txt") as file:
        lines: list[str] = []
        for line in file:
            if line.strip() == "":
                maze = Maze(lines)
                mazes.append(maze)
                lines = []
            else:
                lines.append(line.strip())
        maze = Maze(lines)
        mazes.append(maze)

    return mazes


def main():
    mazes: list[Maze] = read_input()

    for maze in mazes:
        print(maze)
    # q1
    print(sum(maze.score() for maze in mazes))


if __name__ == "__main__":
    main()
