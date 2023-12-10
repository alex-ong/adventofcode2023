from enum import StrEnum


class Color(StrEnum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Draw:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __init__(self, string):
        """string: `1 blue, 4 green, 5 red`"""
        self.parse_colors_count(string)

    def parse_color_count(self, string):
        """string: `1 blue`"""
        num, color = string.split(" ")
        return int(num), Color(color)

    def parse_colors_count(self, string):
        """string: `1 blue, 4 green, 5 red`"""
        for color_count in string.split(","):
            color_count = color_count.strip()
            num, color = self.parse_color_count(color_count)
            if color == Color.RED:
                self.red = num
            elif color == Color.GREEN:
                self.green = num
            elif color == Color.BLUE:
                self.blue = num


class Game:
    id: int
    red: int = 0
    green: int = 0
    blue: int = 0

    def __init__(self, string):
        game_id_str, draw_str = string.split(":")
        self.id = int(game_id_str.replace("Game ", ""))
        self.draws = self.parse_draws(draw_str)
        self.red = max(draw.red for draw in self.draws)
        self.green = max(draw.green for draw in self.draws)
        self.blue = max(draw.blue for draw in self.draws)

    def parse_draws(self, string):
        """string: `1 blue; 4 green, 5 blue; 11 red, 3 blue`"""
        result = []
        for draw_str in string.split(";"):
            draw_str = draw_str.strip()
            draw = Draw(draw_str)
            result.append(draw)
        return result

    def __str__(self):
        return f"Game {self.id}: {self.red},{self.green},{self.blue}"

    def power_level(self):
        return self.red * self.green * self.blue


def game_filter(game: Game):
    """Returns true if the game satisfies the constraints of Question 1"""
    return game.red <= 12 and game.green <= 13 and game.blue <= 14


def main():
    """Parses data into data structures, then prints out answer to q1 and q2"""
    with open("day2.txt", "r", encoding="utf8") as file:
        games = []
        for line in file:
            game = Game(line)
            games.append(game)

    # Q1:
    filtered_games = filter(game_filter, games)
    print(sum(game.id for game in filtered_games))
    # Q2:
    print(sum(game.power_level() for game in games))


if __name__ == "__main__":
    main()
