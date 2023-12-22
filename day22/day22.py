import random
from typing import Any

import vpython
from lib.classes import BoxData, Matrix, Vector3
from lib.parsers_22 import get_boxes

INPUT = "input.txt"
INPUT_SMALL = "input-small.txt"


def construct_box(box_data: BoxData, color: vpython.vector) -> vpython.box:
    return vpython.box(
        pos=box_data.vpos,
        length=box_data.length,
        height=box_data.height,
        width=box_data.width,
        color=color,
    )


def random_color() -> vpython.vector:
    hsv = vpython.vector(random.random(), random.uniform(0.5, 1.0), 1.0)
    return vpython.color.hsv_to_rgb(hsv)


class Visualization:
    boxes: list[BoxData]
    matrix: Matrix
    started: bool

    def __init__(self) -> None:
        self.boxes = get_boxes(INPUT)
        self.boxes.sort(key=lambda x: x.z_val_bot)
        self.matrix = Matrix()
        self.init_vis()
        self.started = False
        vpython.scene.bind("keydown", self.on_key_input)

    def init_vis(self) -> None:
        """Initialize vis boxes"""
        for box in self.boxes:
            color = random_color()
            vbox = construct_box(box, color)
            box.set_vbox(vbox)
        ground = BoxData("ground", Vector3(0, 0, 0), Vector3(10, 10, 0))
        construct_box(ground, random_color())

    def on_key_input(self, evt: Any) -> None:
        character = evt.key
        if character == "shift":
            return
        print(character)
        if character in ["\n", "enter", "return"]:
            self.start()

    def start(self) -> None:
        if self.started:
            return

        for box in self.boxes:
            # vpython.rate(165)
            while self.matrix.can_fall_down(box):
                box.fall()

            self.matrix.register_box(box)
            supports = self.matrix.get_supports(box)
            box.set_supports(supports)

        # have to do this after all boxes dropped
        for box in self.boxes:
            hats = self.matrix.get_hats(box)
            box.set_hats(hats)

        self.started = False

        print(self.calculate_part1())
        print(self.calculate_part2())

    def calculate_part1(self) -> int:
        return sum(1 if self.matrix.can_fly_up(item) else 0 for item in self.boxes)

    def calculate_part2(self) -> int:
        return sum(box.recursive_fall({box}) for box in self.boxes)


def main() -> None:
    vis = Visualization()

    vis.start()  # auto start, comment out and use enter to start

    while True:
        vpython.rate(165)  # we control sleeping
        while vis.started:  # hand over vpython.sleep to vis
            pass


if __name__ == "__main__":
    main()
