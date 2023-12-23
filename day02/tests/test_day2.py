from day02.day2 import INPUT_SMALL, Game, game_filter, get_games, part1, part2


def get_game1() -> Game:
    return Game("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")


def get_game2() -> Game:
    return Game("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue")


def test_game() -> None:
    # constructor:
    game1: Game = get_game1()
    game2: Game = get_game2()

    assert game1.id == 1
    assert game1.red == 4
    assert game1.blue == 6
    assert game1.green == 2

    assert game2.id == 2
    assert game2.red == 1
    assert game2.green == 3
    assert game2.blue == 4


def test_part1() -> None:
    """Tests get_games, game_filter, part1"""
    games: list[Game] = get_games(INPUT_SMALL)

    # test game_filter
    expected: list[bool] = [True, True, False, False, True]
    for index, game in enumerate(games):
        assert game_filter(game) == expected[index]
    # test part1()
    assert part1(games) == 8


def test_part2() -> None:
    """Tests power"""
    games: list[Game] = get_games(INPUT_SMALL)

    # test game_filter
    expected = [48, 12, 1560, 630, 36]
    for index, game in enumerate(games):
        assert game.power_level() == expected[index]
    # test part1()
    assert part2(games) == 2286
