import os
import tempfile
from typing import TYPE_CHECKING

from day20.day20 import FILE_A, FILE_B, FILE_PT2, output_files, part1, part2, simulate
from day20.lib.parsers import get_modules

if TYPE_CHECKING:
    from day20.lib.classes import PulseTarget


def test_day20() -> None:
    modules = get_modules(FILE_A)
    assert part1(modules) == 32000000

    modules = get_modules(FILE_A)

    stored_pulses: list[PulseTarget] = []
    modules_map = {module.name: module for module in modules}
    simulate(modules_map, stored_pulses)
    assert "\n".join(str(pulse) for pulse in stored_pulses) == "\n".join(
        [
            "button -low-> broadcaster",
            "broadcaster -low-> a",
            "broadcaster -low-> b",
            "broadcaster -low-> c",
            "a -high-> b",
            "b -high-> c",
            "c -high-> inv",
            "inv -low-> a",
            "a -low-> b",
            "b -low-> c",
            "c -low-> inv",
            "inv -high-> a",
        ]
    )

    modules = get_modules(FILE_B)
    assert part1(modules) == 11687500


def test_part2() -> None:
    modules = get_modules(FILE_PT2)
    result, dots = part2(modules, True)
    assert result == 495
    with tempfile.TemporaryDirectory(prefix="unit_test_outputs") as temp_dir:
        output_files(dots, temp_dir)
        assert len(os.listdir(temp_dir)) == 16

    # run it without exporting.
    modules = get_modules(FILE_PT2)
    result, dots = part2(modules, False)
    assert result == 495

    with tempfile.TemporaryDirectory(prefix="unit_test_outputs") as temp_dir:
        output_files(dots, temp_dir)
