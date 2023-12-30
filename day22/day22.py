"""Day22 solution."""
import vpython

from day22.lib.classes import BoxData, Matrix
from day22.lib.parsers import get_boxes
from day22.lib.vis import CAMERA_AXIS_1, CAMERA_POS_1, bind_keys, follow_block, init_vis

INPUT = "day22/input.txt"
INPUT_SMALL = "day22/input-small.txt"


AUTO_START = False
ANIMATE = True


class Visualization:
    """Visualization class."""

    boxes: list[BoxData]
    matrix: Matrix
    has_started: bool

    def __init__(self, boxes: list[BoxData], animate: bool = True) -> None:
        """Initialize Vis.

        Args:
            boxes (list[BoxData]): list of boxes to visualize
            animate (bool, optional): Whether to animate the visualizatoin. (Default=True)
        """
        self.boxes = boxes
        self.boxes.sort(key=lambda x: x.z_val_bot)
        self.matrix = Matrix()
        self.animate = animate
        if self.animate:
            init_vis(self.boxes)
            bind_keys(self.start)

        self.has_started = False

    def vis_rate(self, rate: float) -> None:
        """Wait a given amount if we are animating."""
        if self.animate:
            vpython.rate(rate)

    def follow_block(self, y: float, box: BoxData) -> None:
        """Snap camera to a given box."""
        if self.animate:
            follow_block(y, box)

    def start(self) -> None:
        """Start visualization calcuations."""
        if self.has_started:  # pragma: no cover
            return
        self.has_started = True

        if self.animate:
            camera_height = vpython.scene.camera.pos.y
        else:
            camera_height = 0

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
        """Calculate part1. (number of boxes that can fly up)."""
        # short answer
        return sum(1 if self.matrix.can_fly_up(item) else 0 for item in self.boxes)

    def calculate_part2(self) -> int:
        """Calculate part2 (number of boxes that will fall if each box is removed."""
        return sum(len(box.recursive_fall({box})) for box in self.boxes)

    def animate_part1(self) -> None:
        """Animate part 1."""
        if self.animate:
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
        """Animate part2."""
        if self.animate:
            vpython.scene.camera.pos = CAMERA_POS_1
            vpython.scene.camera.axis = CAMERA_AXIS_1
            reversed_boxes = sorted(
                self.boxes, key=lambda box: box.end_pos.z, reverse=True
            )
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
    """Grab boxes and solve, while animating solution."""
    boxes: list[BoxData] = get_boxes(INPUT)
    vis = Visualization(boxes, ANIMATE)

    if AUTO_START:
        vis.start()

    while True:
        vpython.rate(165)  # we control sleeping
        while vis.has_started:  # hand over vpython.sleep to vis
            pass


if __name__ == "__main__":
    main()
