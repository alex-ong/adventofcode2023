"""laser instance class."""
from dataclasses import dataclass

from day16.lib.direction import Direction


@dataclass(frozen=True)  # frozen so we can hash
class Laser:
    """Laser position + direction."""

    row: int
    col: int

    direction: Direction
