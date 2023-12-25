from day15.lib.classes import Box, Lens


def test_box() -> None:
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
