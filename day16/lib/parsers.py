from day16.lib.cells import Cell
from day16.lib.world import World


def get_input(path: str) -> World:
    """Read input file"""
    with open(path) as file:
        all_cells: list[list[Cell]] = []
        for line in file:
            line = line.strip()
            cells = [Cell.construct(char) for char in line]
            all_cells.append(cells)
        world = World(all_cells)
    return world
