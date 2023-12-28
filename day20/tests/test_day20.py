import os
import tempfile

from day20.day20 import FILE_A, FILE_B, FILE_PT2, output_files, part1, part2
from day20.lib.parsers import get_modules


def test_day20() -> None:
    modules = get_modules(FILE_A)
    assert part1(modules) == 32000000

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
