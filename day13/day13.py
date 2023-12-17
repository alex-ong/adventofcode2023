"""day13 solution"""

from dataclasses import dataclass
from typing import Optional


def distance(left: str, right: str) -> int:
    """returns edit distance of two strings"""
    return sum(a != b for a, b in zip(left, right))


@dataclass
class Maze:
    tiles: list[str]

    def solve(self, distance: int = 0) -> int:
        row_reflect = self.reflect_rows(distance)
        col_reflect = self.reflect_cols(distance)
        return self.score(row_reflect, col_reflect)

    def reflect_rows(self, distance: int) -> Optional[int]:
        return self.check_reflection(self.tiles, distance)

    def reflect_cols(self, distance: int) -> Optional[int]:
        """checks reflection of cols by flipping rows/cols"""
        cols: list[list[str]] = [[] for _ in range(len(self.tiles[0]))]
        for row in self.tiles:
            for col_index, col in enumerate(row):
                cols[col_index].append(col)

        cols_strs = ["".join(str(col)) for col in cols]
        return self.check_reflection(cols_strs, distance)

    def check_reflection(self, data: list[str], target_dist: int) -> Optional[int]:
        """Checks a reflection on rows or cols"""
        for index in range(len(data)):
            if index == 0:
                continue

            top_blocks = reversed(data[:index])
            bottom_blocks = data[index:]
            pairs = zip(top_blocks, bottom_blocks)  # accounts for shorter list
            total_diff = sum(distance(top, bottom) for top, bottom in pairs)

            if total_diff == target_dist:
                return index

        return None

    def score(self, row_reflect: Optional[int], col_reflect: Optional[int]) -> int:
        """returns score for q1"""
        if col_reflect is not None:
            return col_reflect
        if row_reflect is not None:
            return 100 * row_reflect
        raise ValueError("expected a mirror!")


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


def main() -> None:
    mazes: list[Maze] = read_input()

    # q1
    print(sum(maze.solve(0) for maze in mazes))

    # q2
    print(sum(maze.solve(distance=1) for maze in mazes))


if __name__ == "__main__":
    main()
