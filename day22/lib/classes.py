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
    box_label: str
    start_pos: Vector3
    end_pos: Vector3
    vbox: vpython.box = field(init=False, repr=False, hash=False)
    supports: set["BoxData"] = field(
        default_factory=set, hash=False
    )  # list of blocks we support

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
    def z_val_bot(self) -> int:
        """return lowest z value (self.start_pos.z)"""
        return self.start_pos.z

    @property
    def z_val_top(self) -> int:
        """return maximum z value(self.end_pos.z)"""
        return self.end_pos.z

    def fall(self) -> None:
        self.start_pos.z -= 1
        self.end_pos.z -= 1
        # vbox y == boxdata z
        self.vbox.pos.y -= 1

    def set_supports(self, supports: set["BoxData"]) -> None:
        self.supports = supports

    def __hash__(self) -> int:
        return hash(f"{self.start_pos} | {self.end_pos}")


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
        if box.z_val_bot == 1:
            return False
        for x in range(box.start_pos.x, box.end_pos.x + 1):
            for y in range(box.start_pos.y, box.end_pos.y + 1):
                if self.layers[box.z_val_bot - 1][x][y] is not None:
                    return False
        return True

    def register_box(self, box: BoxData) -> None:
        """Register box into matrix."""
        for z in range(box.start_pos.z, box.end_pos.z + 1):
            for x in range(box.start_pos.x, box.end_pos.x + 1):
                for y in range(box.start_pos.y, box.end_pos.y + 1):
                    if self.layers[z][x][y] is not None:
                        print("collision at:", (x, y, z))
                        print(f"collision with: {self.layers[z][x][y]}")
                        print(f"trying to insert: {box}")
                        raise ValueError(":o verlap")

                    self.layers[z][x][y] = box

    def get_supports(self, box: BoxData) -> set[BoxData]:
        # return which boxes are supporting this box
        if box.z_val_bot == 1:
            return set()

        supports: set[BoxData] = set()
        for x in range(box.start_pos.x, box.end_pos.x + 1):
            for y in range(box.start_pos.y, box.end_pos.y + 1):
                value = self.layers[box.z_val_bot - 1][x][y]
                if value is not None:
                    supports.add(value)
        return supports

    def can_fly_up(self, box: BoxData) -> bool:
        """Check cells above our block. If they're clear we can fly up"""
        supporting: set[BoxData] = set()  # list of items we're supporting
        for x in range(box.start_pos.x, box.end_pos.x + 1):
            for y in range(box.start_pos.y, box.end_pos.y + 1):
                value = self.layers[box.z_val_top + 1][x][y]
                if value is not None:
                    supporting.add(value)

        # all our "hats" need to have > 1 supports
        hats = list(supporting)
        return all(len(hat.supports) > 1 for hat in hats)
