from day10.day10 import INPUT_A, INPUT_B, INPUT_C, INPUT_D, part1, part2, read_input


def test_day10() -> None:
    pipe_map_a = read_input(INPUT_A)
    pipe_map_b = read_input(INPUT_B)
    # q1
    assert part1(pipe_map_a) == 4
    assert part1(pipe_map_b) == 8

    # q2
    pipe_map_c = read_input(INPUT_C)
    print(pipe_map_c)
    assert part2(pipe_map_c) == 4
    pipe_map_d = read_input(INPUT_D)
    assert part2(pipe_map_d) == 8
