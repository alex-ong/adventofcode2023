from typing import TYPE_CHECKING

from day23.day23 import INPUT_SMALL
from day23.lib.classes import Position
from day23.lib.classes2 import Node, Solver2
from day23.lib.parsers import get_maze

if TYPE_CHECKING:
    from day23.lib.classes import Maze


def test_solver2() -> None:
    maze: Maze = get_maze(INPUT_SMALL)

    # get_nodes
    nodes: dict[Position, Node] = Solver2.get_nodes(maze.copy())
    assert len(nodes) == 9

    # calculate_edges
    start_pos = Position(0, 1)
    Solver2.calculate_edges(nodes[start_pos], nodes, maze.copy())
    assert len(nodes[start_pos].edges) == 1
    assert nodes[start_pos].edges[0].length == 15

    # build_nodes
    solver = Solver2(maze)
    nodes_list: list[Node] = solver.build_nodes()
    print(nodes_list)
    assert len(nodes_list[0].edges) == 1
    assert nodes_list[0].edges[0].length == 15

    assert solver.solve() == 154
