from day18.day18a import INPUT_SMALL, Command, Direction, get_input, get_solution


def test_day18a() -> None:
    commands: list[Command] = get_input(INPUT_SMALL)
    assert len(commands) == 14
    assert commands[0].steps == 6 and commands[0].direction == Direction.Right

    assert get_solution(commands) == 62

    assert str(Direction.Right) == "Right"
