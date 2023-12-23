from typing import TYPE_CHECKING

from day23.day23 import INPUT_SMALL
from day23.lib.classes2 import Node, Solver2
from day23.lib.parsers import get_maze

if TYPE_CHECKING:
    from day23.lib.classes import Maze


def test_solver2() -> None:
    maze: Maze = get_maze(INPUT_SMALL)
    solver2 = Solver2(maze)

    nodes: list[Node] = solver2.build_nodes()

    assert len(nodes) == 9
    assert len(nodes[0].edges) == 1
    assert nodes[0].edges[0].length == 15
