"""Classes for day22."""
from dataclasses import dataclass, field
from typing import Optional

import vpython


@dataclass
class Vector3:
    """Simple 3d vector."""

    x: int
    y: int
    z: int


@dataclass(unsafe_hash=True)
class BoxData:
    """A box in 3d space."""

    name: str = field(hash=True)
    start_pos: Vector3 = field(hash=False)
    end_pos: Vector3 = field(hash=False)
    vbox: Optional[vpython.box] = field(
        init=False, repr=False, hash=False, default=None
    )
    supports: set["BoxData"] = field(
        default_factory=set, hash=False, repr=False, init=False
    )  # list of blocks we support
    hats: set["BoxData"] = field(
        default_factory=set, hash=False, repr=False, init=False
    )
    total_hats: set["BoxData"] = field(
        default_factory=set, hash=False, repr=False, init=False
    )

    @property
    def vpos(self) -> vpython.vector:
        """Pos according to vpython."""
        pos = self.start_pos
        return vpython.vector(
            pos.x + self.length / 2, pos.z + self.height / 2, pos.y + self.width / 2
        )

    @property
    def length(self) -> float:
        """Length according to vpython."""
        return float(self.end_pos.x - self.start_pos.x + 1)

    @property
    def width(self) -> float:
        """Width according to vpython."""
        return float(self.end_pos.y - self.start_pos.y + 1)

    @property
    def height(self) -> float:
        """Height according to vpython."""
        return float(self.end_pos.z - self.start_pos.z + 1)

    @property
    def z_val_bot(self) -> int:
        """Return lowest z value (self.start_pos.z)."""
        return self.start_pos.z

    @property
    def z_val_top(self) -> int:
        """Return maximum z value(self.end_pos.z)."""
        return self.end_pos.z

    ####################################
    # Visualisation calls  (not ci'ed) #
    ####################################
    def set_vbox(self, vbox: vpython.box) -> None:  # pragma: no cover
        """Store a vpython box onto this boxdata."""
        self.vbox = vbox

    def fall(self) -> None:
        """Move block down vertically."""
        self.start_pos.z -= 1
        self.end_pos.z -= 1
        # vbox y == boxdata z
        if self.vbox is not None:  # pragma: no cover
            self.vbox.pos.y -= 1

    def select(self) -> None:
        """Select a box by offsetting it to the side."""
        if self.vbox is not None:  # pragma: no cover
            self.vbox.pos.x += 30
            self.vbox.pos.z -= 30

    def unselect(self) -> None:
        """Unselect a box by putting it back."""
        if self.vbox is not None:  # pragma: no cover
            self.vbox.pos.x -= 30
            self.vbox.pos.z += 30

    ################################################
    # Calculations; supports, hats, recursive fall #
    ################################################

    def set_supports(self, supports: set["BoxData"]) -> None:
        """Set the BoxData's that support us."""
        self.supports = supports

    def set_hats(self, hats: set["BoxData"]) -> None:
        """Set the BoxData's that we support."""
        self.hats = hats

    def recursive_fall(self, already_falling: set["BoxData"]) -> set["BoxData"]:
        """Returns all boxes above us that fall if we fall."""
        to_process: list[BoxData] = []  # items that will fall if this brick is removed
        result: set["BoxData"] = set()
        for hat in self.hats.difference(already_falling):
            remaining_supports = hat.supports.difference(already_falling)
            # if no children support this parent
            if len(remaining_supports) == 0:
                result.add(hat)
                already_falling.add(hat)
                to_process.append(hat)

        # for each parent that falls
        for node in to_process:
            # recursively call chain_remove on this parent
            result.update(node.recursive_fall(already_falling))

        return result


class Matrix:
    """3d matrix."""

    # z, x, y
    layers: list[list[list[Optional[BoxData]]]]

    def __init__(self, z_height: int = 400, xy: int = 10):
        """Initialize based on size."""
        self.layers = []
        for _ in range(z_height):
            layer: list[list[Optional[BoxData]]] = [
                [None for _ in range(xy)] for _ in range(xy)
            ]
            self.layers.append(layer)

    def can_fall_down(self, box: BoxData) -> bool:
        """Whether a given box can fall downwards.

        Args:
            box (BoxData): box to test

        Returns:
            bool: True if the box can fall.
        """
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
                        raise AssertionError("Overlap should not occur")

                    self.layers[z][x][y] = box

    def get_supports(self, box: BoxData) -> set[BoxData]:
        """Return which boxes are supporting this box."""
        if box.z_val_bot == 1:
            return set()

        supports: set[BoxData] = set()
        for x in range(box.start_pos.x, box.end_pos.x + 1):
            for y in range(box.start_pos.y, box.end_pos.y + 1):
                value = self.layers[box.z_val_bot - 1][x][y]
                if value is not None:
                    supports.add(value)
        return supports

    def get_hats(self, box: BoxData) -> set[BoxData]:
        """Return which boxes are resting on this box."""
        hats: set[BoxData] = set()  # list of items we're supporting
        for x in range(box.start_pos.x, box.end_pos.x + 1):
            for y in range(box.start_pos.y, box.end_pos.y + 1):
                value = self.layers[box.z_val_top + 1][x][y]
                if value is not None:
                    hats.add(value)
        return hats

    def can_fly_up(self, box: BoxData) -> bool:
        """Check cells above our block. If they're clear we can fly up."""
        # all our "hats" need to have > 1 supports
        hats = list(box.hats)
        return all(len(hat.supports) > 1 for hat in hats)
