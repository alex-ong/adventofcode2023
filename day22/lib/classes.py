from dataclasses import dataclass, field
from typing import Optional

import vpython


@dataclass
class Vector3:
    x: int
    y: int
    z: int


@dataclass
class BoxData:
    start_pos: Vector3
    end_pos: Vector3
    vbox: vpython.box = field(init=False, repr=False)

    @property
    def vpos(self) -> vpython.vector:
        pos = self.start_pos
        return vpython.vector(
            pos.x + self.length / 2, pos.z + self.height / 2, pos.y + self.width / 2
        )

    @property
    def length(self) -> float:
        return float(self.end_pos.x - self.start_pos.x + 1)

    @property
    def width(self) -> float:
        return float(self.end_pos.y - self.start_pos.y + 1)

    @property
    def height(self) -> float:
        return float(self.end_pos.z - self.start_pos.z + 1)

    def set_vbox(self, vbox: vpython.box) -> None:
        self.vbox = vbox

    @property
    def z_val(self) -> int:
        """return lowest z value (self.start_pos.z)"""
        return self.start_pos.z

    def fall(self) -> None:
        self.start_pos.z -= 1
        self.end_pos.z -= 1
        # vbox y == boxdata z
        self.vbox.pos.y -= 1


class Matrix:
    # z, x, y
    layers: list[list[list[Optional[BoxData]]]]

    def __init__(self, z_height: int = 400, xy: int = 10):
        self.layers = []
        for _ in range(z_height):
            layer: list[list[Optional[BoxData]]] = [
                [None for _ in range(xy)] for _ in range(xy)
            ]
            self.layers.append(layer)

    def can_fall_down(self, box: BoxData) -> bool:
        if box.z_val == 1:
            return False
        for x in range(box.start_pos.x, box.end_pos.x + 1):
            for y in range(box.start_pos.y, box.end_pos.y + 1):
                if self.layers[box.z_val - 1][x][y] is not None:
                    return False
        return True

    def register_box(self, box: BoxData) -> None:
        for z in range(box.start_pos.z, box.end_pos.z + 1):
            for x in range(box.start_pos.x, box.end_pos.x + 1):
                for y in range(box.start_pos.y, box.end_pos.y + 1):
                    if self.layers[z][x][y] is not None:
                        print(self.layers[z][x][y])
                        raise ValueError(":o verlap")
                    self.layers[z][x][y] = box
