"""day2 solution."""
from enum import StrEnum

INPUT = "day02/input.txt"
INPUT_SMALL = "day02/input-small.txt"


class Color(StrEnum):
    """Color enum."""

    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Draw:
    """Class representing a draw from the bag."""

    red: int = 0
    green: int = 0
    blue: int = 0

    def __init__(self, string: str):
        """string: ``1 blue, 4 green, 5 red``."""
        self.parse_colors_count(string)

    def parse_color_count(self, string: str) -> tuple[int, Color]:
        """string: ``1 blue``."""
        num, color = string.split(" ")
        return int(num), Color(color)

    def parse_colors_count(self, string: str) -> None:
        """string: ``1 blue, 4 green, 5 red``."""
        for color_count in string.split(","):
            color_count = color_count.strip()
            num, color = self.parse_color_count(color_count)
            if color == Color.RED:
                self.red = num
            elif color == Color.GREEN:
                self.green = num
            else:  # color == Color.BLUE:
                self.blue = num


class Game:
    """Game class, showing multiple draws."""

    id: int
    red: int = 0
    green: int = 0
    blue: int = 0

    def __init__(self, string: str):
        """Create a game from an input string.

        Args:
            string (str): a game string
        """
        game_id_str, draw_str = string.split(":")
        self.id = int(game_id_str.replace("Game ", ""))
        self.draws = self.parse_draws(draw_str)
        self.red = max(draw.red for draw in self.draws)
        self.green = max(draw.green for draw in self.draws)
        self.blue = max(draw.blue for draw in self.draws)

    def parse_draws(self, string: str) -> list[Draw]:
        """string: ``1 blue; 4 green, 5 blue; 11 red, 3 blue``."""
        result = []
        for draw_str in string.split(";"):
            draw_str = draw_str.strip()
            draw = Draw(draw_str)
            result.append(draw)
        return result

    def __str__(self) -> str:
        """Return summary of game id and minimal rgb."""
        return f"Game {self.id}: {self.red},{self.green},{self.blue}"

    def power_level(self) -> int:
        """Returns r*g*b."""
        return self.red * self.green * self.blue


def game_filter(game: Game) -> bool:
    """Returns true if the game satisfies the constraints of Question 1."""
    return game.red <= 12 and game.green <= 13 and game.blue <= 14


def get_games(input_file: str) -> list[Game]:
    """Gets the games from the input file.

    Args:
        input_file (str): input file name

    Returns:
        list[Game]: list of Games
    """
    with open(input_file, "r", encoding="utf8") as file:
        games: list[Game] = []
        for line in file:
            game = Game(line)
            games.append(game)
    return games


def part1(games: list[Game]) -> int:
    """Solves part 1."""
    filtered_games = filter(game_filter, games)
    return sum(game.id for game in filtered_games)


def part2(games: list[Game]) -> int:
    """Solves part2."""
    return sum(game.power_level() for game in games)


def main() -> None:
    """Parses data into data structures, then prints out answer to q1 and q2."""
    games = get_games(INPUT)

    # Q1:
    print(part1(games))

    # Q2:
    print(part2(games))


if __name__ == "__main__":
    main()
