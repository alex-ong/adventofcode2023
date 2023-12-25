from day18.day18b import INPUT_SMALL, Command, Direction, get_input, get_solution


def test_day18b() -> None:
    commands: list[Command] = get_input(INPUT_SMALL)
    assert len(commands) == 14
    assert commands[0].steps == 461937 and commands[0].direction == Direction.Right
    assert commands[1].steps == 56407 and commands[1].direction == Direction.Down

    assert get_solution(commands) == 952408144115


def test_command() -> None:
    assert Command("70c710").steps == 461937
    assert Command("0dc571").steps == 56407
    assert Command("5713f0").steps == 356671
    assert Command("d2c081").steps == 863240
    assert Command("59c680").steps == 367720
    assert Command("411b91").steps == 266681
    assert Command("8ceee2").steps == 577262
    assert Command("caa173").steps == 829975
    assert Command("1b58a2").steps == 112010
    assert Command("caa171").steps == 829975
    assert Command("7807d2").steps == 491645
    assert Command("a77fa3").steps == 686074
    assert Command("015232").steps == 5411
    assert Command("7a21e3").steps == 500254

    assert Command("70c710").direction == Direction.Right
    assert Command("0dc571").direction == Direction.Down
    assert Command("5713f0").direction == Direction.Right
    assert Command("d2c081").direction == Direction.Down
    assert Command("59c680").direction == Direction.Right
    assert Command("411b91").direction == Direction.Down
    assert Command("8ceee2").direction == Direction.Left
    assert Command("caa173").direction == Direction.Up
    assert Command("1b58a2").direction == Direction.Left
    assert Command("caa171").direction == Direction.Down
    assert Command("7807d2").direction == Direction.Left
    assert Command("a77fa3").direction == Direction.Up
    assert Command("015232").direction == Direction.Left
    assert Command("7a21e3").direction == Direction.Up
