from day22.day22 import INPUT_SMALL
from day22.lib.classes import BoxData, Vector3
from day22.lib.parsers import get_boxes


def test_parser() -> None:
    boxes: list[BoxData] = get_boxes(INPUT_SMALL)
    assert len(boxes) == 7
    assert boxes[0].start_pos == Vector3(1, 0, 1)
    assert boxes[0].end_pos == Vector3(1, 2, 1)
