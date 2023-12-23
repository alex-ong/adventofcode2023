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


CAMERA_START = vpython.vector(40.0164, 11.0337, 39.9238)
CAMERA_AXIS = -CAMERA_START

CAMERA_POS_1 = vpython.vector(111.512, 122.347, 65.0144)
CAMERA_AXIS_1 = vpython.vector(-83.3746, -20.0517, -69.4084)


class Visualization:
    boxes: list[BoxData]
    matrix: Matrix
    has_started: bool

    def __init__(self, auto_start: bool = False, animate: bool = True) -> None:
        self.boxes = get_boxes(INPUT)
        self.boxes.sort(key=lambda x: x.z_val_bot)
        self.matrix = Matrix()
        self.init_vis()
        self.has_started = False
        vpython.scene.bind("keydown", self.on_key_input)
        self.animate = animate
        if auto_start:
            self.start()

    def init_vis(self) -> None:
        """Initialize vis boxes"""
        for box in self.boxes:
            color = random_color()
            vbox = construct_box(box, color)
            box.set_vbox(vbox)
        ground = BoxData("ground", Vector3(0, 0, 0), Vector3(10, 10, 0))
        construct_box(ground, random_color())
        # init camera:
        vpython.scene.camera.axis = CAMERA_AXIS
        vpython.scene.camera.pos = CAMERA_START
        vpython.scene.height = 600
        vpython.scene.width = 400

    def on_key_input(self, evt: Any) -> None:
        character = evt.key
        if character == "shift":
            return
        print(character)
        if character in ["\n", "enter", "return"]:
            self.start()
        if character == "c":
            print(vpython.scene.camera.pos)
            print(vpython.scene.camera.axis)

    def vis_sleep(self, time: float) -> None:
        if self.animate:
            vpython.sleep(time)

    def vis_rate(self, rate: float) -> None:
        if self.animate:
            vpython.rate(rate)

    def follow_block(self, y: float, box: BoxData) -> None:
        pos = vpython.scene.camera.pos
        pos.y = max(y + box.start_pos.z, pos.y)
        vpython.scene.camera.pos = pos

    def start(self) -> None:
        if self.has_started:
            return
        self.has_started = True
        camera_height = vpython.scene.camera.pos.y

        for box in self.boxes:
            while self.matrix.can_fall_down(box):
                box.fall()
            self.vis_rate(165)
            self.matrix.register_box(box)
            supports = self.matrix.get_supports(box)
            box.set_supports(supports)
            self.follow_block(camera_height, box)

        # have to do this after all boxes dropped
        for box in self.boxes:
            hats = self.matrix.get_hats(box)
            box.set_hats(hats)

        print(self.calculate_part1())
        print(self.calculate_part2())
        self.animate_part1()
        self.animate_part2()

    def calculate_part1(self) -> int:
        # short answer
        return sum(1 if self.matrix.can_fly_up(item) else 0 for item in self.boxes)

    def calculate_part2(self) -> int:
        return sum(len(box.recursive_fall({box})) for box in self.boxes)

    def animate_part1(self) -> None:
        if not self.animate:
            return
        vpython.scene.camera.pos = CAMERA_POS_1
        vpython.scene.camera.axis = CAMERA_AXIS_1
        for box in self.boxes:
            if self.matrix.can_fly_up(box):
                box.select()
                self.vis_rate(60)

        for box in self.boxes:
            if self.matrix.can_fly_up(box):
                box.unselect()
                self.vis_rate(60)

    def animate_part2(self) -> None:
        if not self.animate:
            return
        vpython.scene.camera.pos = CAMERA_POS_1
        vpython.scene.camera.axis = CAMERA_AXIS_1
        reversed_boxes = sorted(self.boxes, key=lambda box: box.end_pos.z, reverse=True)
        for box in reversed_boxes:
            to_fall = box.recursive_fall({box})
            to_fall_sorted = sorted(to_fall, key=lambda x: x.z_val_bot)
            if len(to_fall_sorted) == 0:
                continue

            for faller in to_fall_sorted:
                faller.select()

            self.vis_rate(20)

            for faller in to_fall:
                faller.unselect()


def main() -> None:
    auto_start = True
    vis = Visualization(auto_start, True)

    while True:
        vpython.rate(165)  # we control sleeping
        while vis.has_started:  # hand over vpython.sleep to vis
            pass


if __name__ == "__main__":
    main()
