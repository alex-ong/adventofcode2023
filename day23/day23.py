from queue import Queue
from typing import Optional

from day23.lib.classes import Maze, Path, Position
from day23.lib.parsers import get_maze

INPUT = "day23/input.txt"
INPUT_SMALL = "day23/input-small.txt"


class Solver:
    maze: Maze
    handle_hills: bool

    def __init__(self, maze: Maze, handle_hills: bool = True) -> None:
        self.maze = maze
        self.handle_hills = handle_hills

    def solve(self) -> list[Path]:
        paths: Queue[Path] = Queue()
        first_path = Path()
        first_path.add(Position(0, 1))
        paths.put(first_path)
        # bfs all paths simultaneously
        results: list[Path] = []
        while not paths.empty():
            path = paths.get()
            if path.last().row == self.maze.num_rows - 1:
                results.append(path)
                continue

            for expansion in self.expand_path(path):
                paths.put(expansion)
        return results

    def expand_hill(self, position: Position, tile: str) -> list[Position]:
        if tile == "^":
            return [position.copy_modify(row=-1)]
        elif tile == "v":
            return [position.copy_modify(row=+1)]
        elif tile == "<":
            return [position.copy_modify(col=-1)]
        elif tile == ">":
            return [position.copy_modify(col=+1)]
        else:
            return position.expand()

    def expand_path(self, path: Path) -> list[Path]:
        current_pos: Position = path.last()
        current_tile: Optional[str] = self.maze[current_pos]
        if current_tile is None:
            raise ValueError("there's no shot we got a tile outside the maze")
        expansions: list[Position]
        if self.handle_hills:
            expansions = self.expand_hill(current_pos, current_tile)
        else:
            expansions = current_pos.expand()

        valid_expansions = []
        for expansion in expansions:
            expansion_tile = self.maze[expansion]
            if (
                path.can_add(expansion)
                and expansion_tile is not None
                and expansion_tile != "#"
            ):
                valid_expansions.append(expansion)

        if len(valid_expansions) == 0:
            return []
        elif len(valid_expansions) == 1:
            path.add(valid_expansions[0])
            return [path]
        else:
            result = []
            for expansion in valid_expansions[1:]:
                new_path = path.copy()
                new_path.add(expansion)
                result.append(new_path)
            path.add(valid_expansions[0])
            result.append(path)
            return result


def part1(maze: Maze) -> int:
    return solve(maze, True)


def solve(maze: Maze, handle_hills: bool) -> int:
    solver = Solver(maze, handle_hills)
    paths: list[Path] = solver.solve()
    path_lengths = [len(path) for path in paths]
    path_lengths.sort(reverse=True)
    return path_lengths[0]


def main() -> None:
    maze: Maze = get_maze(INPUT)

    print(part1(maze))


if __name__ == "__main__":
    main()
