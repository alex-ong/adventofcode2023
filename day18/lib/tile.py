from dataclasses import dataclass


@dataclass
class Tile:
    contents: str = "."

    def __str__(self) -> str:
        return self.contents


@dataclass(kw_only=True)
class EdgeTile(Tile):
    contents: str = "#"
    color: str

    # 38 -> 48 for background
    TEXT_WHITE = "\033[38;2;255;255;255m"

    def text_color(self, r: int, g: int, b: int) -> str:
        return f"\033[38;2;{r};{g};{b}m"

    def __str__(self) -> str:
        r, g, b = [int(self.color[i * 2 : i * 2 + 2], 16) for i in range(3)]

        return f"{self.text_color(r,g,b)}{self.contents}{self.TEXT_WHITE}"


@dataclass(kw_only=True)
class HoleTile(Tile):
    contents: str = " "
