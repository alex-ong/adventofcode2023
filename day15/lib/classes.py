"""Classes for day15."""
from dataclasses import dataclass, field
from enum import IntEnum


class AddRemove(IntEnum):
    """Simple instruction to add or remove lens."""

    Add = 0
    Remove = 1


@dataclass
class Step:
    """well defined step."""

    lens_name: str
    box: int
    process: AddRemove
    focal_length: int | None = None


@dataclass
class Lens:
    """Lens object."""

    name: str
    focal_length: int

    def __hash__(self) -> int:  # pragma: no cover
        """Custom hash function for use with ``set()``."""
        return hash(str(self.name) + ":" + str(self.focal_length))

    def __str__(self) -> str:
        """Custom compact string representation."""
        return f"[{self.name} {self.focal_length}]"


@dataclass
class Box:
    """Box can contain a variety of ``Lens``es."""

    id: int = 0
    contents: list[Lens] = field(default_factory=list)

    def add_lens(self, lens: Lens) -> None:
        """Add/replace a lens to this box.

        If a lens name already exists, swap its power;
        otherwise just add it
        """
        for existing_lens in self.contents:
            if lens.name == existing_lens.name:
                existing_lens.focal_length = lens.focal_length
                return
        self.contents.append(lens)

    def remove_lens(self, lens_name: str) -> None:
        """If a lens with a matching name is inside, remove it."""
        to_remove = None
        for existing_lens in self.contents:
            if existing_lens.name == lens_name:
                to_remove = existing_lens
                break
        if to_remove is not None:
            self.contents.remove(to_remove)

    def __str__(self) -> str:
        """Custom string for our box to see its id/contents easily."""
        return f"Box {self.id}: " + " ".join(str(lens) for lens in self.contents)

    def calculate_power(self) -> int:
        """Calculates power of the box by summing powers of the lenses."""
        result = 0
        for slot_number, lens in enumerate(self.contents):
            box_power = 1 + self.id
            slot_power = slot_number + 1
            power = box_power * slot_power * lens.focal_length
            result += power

        return result
