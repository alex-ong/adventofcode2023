"""Tests classes for day15."""
from day15.lib.classes import Box, Lens


def test_box() -> None:
    """Test box class."""
    box = Box(0)
    rn = Lens("rn", 1)
    box.add_lens(rn)
    assert box.contents == [rn]
    cm = Lens("cm", 2)
    box.add_lens(cm)
    assert box.contents == [rn, cm]

    box = Box(3)
    box.add_lens(pc := Lens("pc", 4))
    box.add_lens(ot := Lens("ot", 9))
    box.add_lens(ab := Lens("ab", 5))
    assert box.contents == [pc, ot, ab]
    box.remove_lens("pc")
    assert box.contents == [ot, ab]
    box.add_lens(pc := Lens("pc", 6))
    assert box.contents == [ot, ab, pc]
    box.add_lens(ot2 := Lens("ot", 7))
    assert box.contents == [ot2, ab, pc]
    assert box.contents[0].focal_length == 7

    assert str(box) == "Box 3: [ot 7] [ab 5] [pc 6]"


def test_lens() -> None:
    """Tests lens class."""
    lens: Lens = Lens("rn", 1)
    assert lens.focal_length == 1
    assert lens.name == "rn"
    assert str(lens) == "[rn 1]"
