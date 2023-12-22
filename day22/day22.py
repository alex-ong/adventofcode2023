import random
from typing import Any

import vpython
from lib.classes import BoxData, Vector3
from lib.parsers_22 import get_boxes


def construct_box(box_data: BoxData, color: vpython.vector) -> vpython.box:
    return vpython.box(
        pos=box_data.vpos,
        length=box_data.length,
        height=box_data.height,
        width=box_data.width,
        color=color,
        make_trail=True,
    )


def random_color() -> vpython.vector:
    hsv = vpython.vector(random.random(), random.uniform(0.5, 1.0), 1.0)
    return vpython.color.hsv_to_rgb(hsv)


class Visualization:
    boxes: list[BoxData]

    def __init__(self) -> None:
        self.boxes = get_boxes()

        self.init_vis()
        vpython.scene.bind("keydown", self.on_key_input)

    def init_vis(self) -> None:
        """Initialize vis boxes"""
        for box in self.boxes:
            color = random_color()
            vbox = construct_box(box, color)
            box.set_vbox(vbox)
        ground = BoxData(Vector3(0, 0, 0), Vector3(10, 10, 0))
        construct_box(ground, random_color())

    def on_key_input(self, evt: Any) -> None:
        character = evt.key
        if character == "shift":
            return
        print(character)

    def start(self) -> None:
        while True:
            vpython.rate(30)


def main() -> None:
    vis = Visualization()
    vis.start()


if __name__ == "__main__":
    main()