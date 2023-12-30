"""Test main functions of day22."""
from typing import TYPE_CHECKING

from day22.day22 import INPUT_SMALL, Visualization
from day22.lib.parsers import get_boxes

if TYPE_CHECKING:
    from day22.lib.classes import BoxData


def test_visualization() -> None:
    """Tests results from day22 vis class."""
    boxes: list[BoxData] = get_boxes(INPUT_SMALL)
    vis = Visualization(boxes, False)

    vis.start()
    assert vis.calculate_part1() == 5
    assert vis.calculate_part2() == 7
