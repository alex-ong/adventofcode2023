"""Day15 main functions."""
from day15.day15 import (
    INPUT_SMALL,
    get_input,
    get_string_hash,
    parse_step_pt2,
    question1,
    question2,
)
from day15.lib.classes import AddRemove, Step


def test_get_input() -> None:
    """Test reading input function."""
    steps: list[str] = get_input(INPUT_SMALL)
    assert len(steps) == 11
    assert steps[0] == "rn=1"


def test_parse_pt2() -> None:
    """Test parsing input for part2."""
    steps: list[str] = get_input(INPUT_SMALL)
    step: Step = parse_step_pt2(steps[0])
    assert step.lens_name == "rn"
    assert step.process == AddRemove.Add


def test_questions() -> None:
    """Test question1/question2."""
    steps: list[str] = get_input(INPUT_SMALL)
    assert question1(steps) == 1320
    assert question2(steps) == 145


def test_get_string_hash() -> None:
    """Test string hashing function."""
    assert get_string_hash("rn=1") == 30
    assert get_string_hash("rn=1") == 30
    assert get_string_hash("cm-") == 253
    assert get_string_hash("qp=3") == 97
    assert get_string_hash("cm=2") == 47
    assert get_string_hash("qp-") == 14
    assert get_string_hash("pc=4") == 180
    assert get_string_hash("ot=9") == 9
    assert get_string_hash("ab=5") == 197
    assert get_string_hash("pc-") == 48
    assert get_string_hash("pc=6") == 214
    assert get_string_hash("ot=7") == 231
