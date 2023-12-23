from dataclasses import dataclass

from day03.classes import PartNumber


@dataclass
class PartNumberTouchTest:
    col: int
    row: int
    row_size: int
    result: bool


def test_part_number() -> None:
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
