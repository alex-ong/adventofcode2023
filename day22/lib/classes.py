from dataclasses import dataclass, field

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
