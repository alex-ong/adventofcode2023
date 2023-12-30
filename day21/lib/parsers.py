"""Parsing code for day21."""
from day21.lib.classes import Maze, Position


def parse_maze(filename: str) -> tuple[Position, Maze]:
    """Returns a well defined Maze class."""
    maze_rows: list[str] = []
    with open(filename, encoding="utf8") as file:
        for row, line in enumerate(file):
            line = line.strip()
            if "S" in line:
                col = line.index("S")
                start_pos = Position(row, col)
            maze_rows.append(line)
    if start_pos is None:
        raise AssertionError("no start position!")
    return start_pos, Maze(maze_rows)
