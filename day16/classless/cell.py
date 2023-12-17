from typing import Iterable

from direction import EAST, NORTH, SOUTH, WEST


def dot(row, col, direction):
    if direction == EAST:
        return [(row, col + 1, direction)]
    if direction == WEST:
        return [(row, col - 1, direction)]
    if direction == NORTH:
        return [(row - 1, col, direction)]
    if direction == SOUTH:
        return [(row + 1, col, direction)]


def pipe(row, col, direction):
    if direction == NORTH:
        return [(row - 1, col, direction)]
    if direction == SOUTH:
        return [(row + 1, col, direction)]
    return [
        (row - 1, col, NORTH),
        (row + 1, col, SOUTH),
    ]


def dash(row, col, direction):
    if direction == EAST:
        return [(row, col + 1, direction)]
    if direction == WEST:
        return [(row, col - 1, direction)]
    return [
        (row, col + 1, EAST),
        (row, col - 1, WEST),
    ]


def slash(row, col, direction):
    if direction == EAST:
        return [(row - 1, col, NORTH)]
    if direction == WEST:
        return [(row + 1, col, SOUTH)]
    if direction == NORTH:
        return [(row, col + 1, EAST)]
    if direction == SOUTH:
        return [(row, col - 1, WEST)]


def backslash(row, col, direction):
    if direction == EAST:
        return [(row + 1, col, SOUTH)]
    if direction == WEST:
        return [(row - 1, col, NORTH)]
    if direction == NORTH:
        return [(row, col - 1, WEST)]
    if direction == SOUTH:
        return [(row, col + 1, EAST)]


def next_lasers(
    contents: str, row: int, col: int, direction: int
) -> Iterable[tuple[int, int, int]]:
    if contents == ".":
        return dot(row, col, direction)

    if contents == "|":
        return pipe(row, col, direction)

    if contents == "-":
        return dash(row, col, direction)

    if contents == "/":
        return slash(row, col, direction)
    if contents == "\\":
        return backslash(row, col, direction)
    raise ValueError(f"Unexpected contents: {contents}")
