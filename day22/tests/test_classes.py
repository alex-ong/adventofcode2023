from typing import TYPE_CHECKING

from day22.lib.classes import BoxData, Vector3

if TYPE_CHECKING:
    import vpython


def test_box_data() -> None:
    start: Vector3 = Vector3(1, 1, 1)
    end: Vector3 = Vector3(1, 4, 1)
    box: BoxData = BoxData("memes", start, end)
    vec: vpython.vector = box.vpos
    # our source z is vpython's y
    assert vec.x == 1.5
    assert vec.z == 3.0
    assert vec.y == 1.5
