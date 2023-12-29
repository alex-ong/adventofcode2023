"""tests day3's classes."""
from dataclasses import dataclass

import pytest

from day03.day3 import INPUT_SMALL
from day03.lib.classes import Gear, Matrix, PartNumber
from day03.lib.parsers import get_matrix


@dataclass
class PartNumberTouchTest:
    """Result for a part number touching something else."""

    col: int
    row: int
    row_size: int
    result: bool


def test_part_number() -> None:
    """Tests part number class."""
    part_number = PartNumber(0, 0, 3, 467)

    assert part_number.end_index == 3

    tests = [
        PartNumberTouchTest(0, 0, 10, True),
        PartNumberTouchTest(0, 0, 10, True),
        PartNumberTouchTest(1, 0, 10, True),
        PartNumberTouchTest(2, 0, 10, True),
        PartNumberTouchTest(3, 0, 10, True),
        PartNumberTouchTest(0, 0, 10, True),
        PartNumberTouchTest(1, 1, 10, True),
        PartNumberTouchTest(2, 1, 10, True),
        PartNumberTouchTest(3, 1, 10, True),
        PartNumberTouchTest(1, -1, 10, True),
        PartNumberTouchTest(2, -1, 10, True),
        PartNumberTouchTest(3, -1, 10, True),
        PartNumberTouchTest(4, 0, 10, False),
    ]
    for test in tests:
        assert part_number.touching(test.col, test.row, test.row_size) == test.result


def test_matrix() -> None:
    """Tests matrix."""
    matrix: Matrix = get_matrix(INPUT_SMALL)
    part_numbers: list["PartNumber"] = matrix.get_part_numbers()
    assert (matrix.row_count, matrix.row_size) == (10, 10)
    assert len(part_numbers) == 10
    part_numbers = matrix.filter_engine_parts(part_numbers)
    assert len(part_numbers) == 8

    assert not Matrix.is_engine_part_row("123.24.56")
    assert Matrix.is_engine_part_row("123.#24.56")
    assert Matrix.is_engine_part_row("123.*24.56")

    gears: list[Gear] = matrix.get_gears(part_numbers)

    assert len(gears) == 3

    matrix2: Matrix = Matrix(["*755."])
    assert matrix2.is_engine_part(PartNumber(1, 0, 3, 755))


def test_gear() -> None:
    """Tests gear class."""
    # 69...
    # ..*78
    # 54...
    part_number1 = PartNumber(0, 0, 2, 69)
    part_number2 = PartNumber(3, 1, 2, 78)
    part_number3 = PartNumber(0, 2, 2, 54)

    gear1 = Gear(1, 2, [part_number1])
    gear2 = Gear(1, 2, [part_number1, part_number2])
    gear3 = Gear(1, 2, [part_number1, part_number2, part_number3])

    assert gear1.gear_ratio == 0
    assert gear2.gear_ratio == 69 * 78
    assert gear3.gear_ratio == 0

    gear_not_init = Gear(1, 1)

    with pytest.raises(ValueError):
        gear_not_init.gear_ratio
