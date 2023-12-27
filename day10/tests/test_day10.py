from typing import TYPE_CHECKING

import pytest

from day10.day10 import (
    INPUT_A,
    INPUT_B,
    INPUT_C,
    INPUT_D,
    calculate_s,
    expand_pipe,
    find_s,
    part1,
    part2,
    read_input,
)
from day10.lib.position import Position

INPUT_E = "day10/tests/input-e.txt"
INPUT_F = "day10/tests/input-f.txt"


if TYPE_CHECKING:
    from day10.lib.pipes import PipeMap


def test_day10() -> None:
    pipe_map_a: PipeMap = read_input(INPUT_A)
    pipe_map_b: PipeMap = read_input(INPUT_B)
    # q1
    assert part1(pipe_map_a) == 4
    assert part1(pipe_map_b) == 8

    s_pos: Position = find_s(pipe_map_b)
    assert s_pos == Position(2, 0)
    assert calculate_s(s_pos, pipe_map_b) == "F"

    # q2
    pipe_map_c: PipeMap = read_input(INPUT_C)
    assert part2(pipe_map_c) == 4
    pipe_map_d: PipeMap = read_input(INPUT_D)
    assert part2(pipe_map_d) == 8

    # pipe_map no s
    pipe_map_no_s: PipeMap = read_input(INPUT_E)
    with pytest.raises(AssertionError):
        s_pos = find_s(pipe_map_no_s)

    # pipe map, s is incalculable
    pipe_map_bad_s: PipeMap = read_input(INPUT_F)
    s_pos = find_s(pipe_map_bad_s)

    with pytest.raises(ValueError):
        calculate_s(s_pos, pipe_map_no_s)

    with pytest.raises(ValueError):
        expand_pipe("^", True)

    with pytest.raises(ValueError):
        pipe_map_bad_s.get_pipe(Position(-1, -1))
