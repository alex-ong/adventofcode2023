from day23.lib.classes import Maze


def get_maze(path: str) -> Maze:
    rows: list[list[str]] = []
    with open(path, encoding="utf8") as file:
        rows = [list(line.strip()) for line in file]
    return Maze(rows)