"""Visualization classes."""
import random
from typing import Any

import vpython

from day22.lib.classes import BoxData, Matrix, Vector3


def construct_box(box_data: BoxData, color: vpython.vector) -> vpython.box:
    """Constructs a vpython box from a box_data.

    Args:
        box_data (BoxData): box data to mimic
        color (vpython.vector): color of box for vis.

    Returns:
        vpython.box: a vpython.box
    """
    return vpython.box(
        pos=box_data.vpos,
        length=box_data.length,
        height=box_data.height,
        width=box_data.width,
        color=color,
    )


def random_color() -> vpython.vector:
    """Returns a random color compatible with vpython."""
    hsv = vpython.vector(random.random(), random.uniform(0.5, 1.0), 1.0)
    return vpython.color.hsv_to_rgb(hsv)


CAMERA_START = vpython.vector(40.0164, 11.0337, 39.9238)
CAMERA_AXIS = -CAMERA_START

CAMERA_POS_1 = vpython.vector(111.512, 122.347, 65.0144)
CAMERA_AXIS_1 = vpython.vector(-83.3746, -20.0517, -69.4084)


def init_vis(boxes: list[BoxData]) -> None:
    """Initialize vis boxes. Only called if we're visualizing."""
    for box in boxes:
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


def bind_keys(on_key_down: Any) -> None:
    """Bind keyboard events, so that ``enter`` calls the given callback."""

    def callback(evt: Any) -> None:
        character = evt.key
        if character == "shift":
            return
        print(character)
        if character in ["\n", "enter", "return"]:
            on_key_down()

    vpython.scene.bind("keydown", callback)


def follow_block(y: float, box: BoxData) -> None:
    """Force camera to follow a block."""
    pos = vpython.scene.camera.pos
    pos.y = max(y + box.start_pos.z, pos.y)
    vpython.scene.camera.pos = pos


def animate_part1(boxes: list[BoxData], matrix: Matrix) -> None:
    """Animates part1."""
    vpython.scene.camera.pos = CAMERA_POS_1
    vpython.scene.camera.axis = CAMERA_AXIS_1
    for box in boxes:
        if matrix.can_fly_up(box):
            box.select()
            vpython.rate(60)

    for box in boxes:
        if matrix.can_fly_up(box):
            box.unselect()
            vpython.rate(60)


def animate_part2(boxes: list[BoxData]) -> None:
    """Animates part2."""
    vpython.scene.camera.pos = CAMERA_POS_1
    vpython.scene.camera.axis = CAMERA_AXIS_1
    reversed_boxes = sorted(boxes, key=lambda box: box.end_pos.z, reverse=True)
    for box in reversed_boxes:
        to_fall = box.recursive_fall({box})
        to_fall_sorted = sorted(to_fall, key=lambda x: x.z_val_bot)
        if len(to_fall_sorted) == 0:
            continue

        for faller in to_fall_sorted:
            faller.select()

        vpython.rate(20)

        for faller in to_fall:
            faller.unselect()
