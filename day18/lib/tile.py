"""Tile Class."""
from dataclasses import dataclass


@dataclass
class Tile:
    """Tile for part 1, represents a non-dugout tile."""

    contents: str = "."

    def __str__(self) -> str:
        """Custom str for easy printing."""
        return self.contents


@dataclass(kw_only=True)
class EdgeTile(Tile):
    """Edge tile (``#``)."""

    contents: str = "#"
    color: str

    # 38 -> 48 for background
    TEXT_WHITE = "\033[38;2;255;255;255m"

    def text_color(self, r: int, g: int, b: int) -> str:
        """Return ansicode color of edge based on input."""
        return f"\033[38;2;{r};{g};{b}m"

    def __str__(self) -> str:
        """Return colored string of ``#`` based on hexcode."""
        r, g, b = [int(self.color[i * 2 : i * 2 + 2], 16) for i in range(3)]

        return f"{self.text_color(r,g,b)}{self.contents}{self.TEXT_WHITE}"


@dataclass(kw_only=True)
class HoleTile(Tile):
    """Dug out tile."""

    contents: str = " "
