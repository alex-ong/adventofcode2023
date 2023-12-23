from day23.lib.parsers import get_maze
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from day23.lib.classes import Maze

INPUT = "day23/input.txt"
INPUT_SMALL = "day23/input-small.txt"


def main() -> None:
    maze: Maze = get_maze(INPUT_SMALL)
    print(maze)


if __name__ == "__main__":
    main()
