from typing import TYPE_CHECKING

from day03.day3 import INPUT_SMALL, part1, part2
from day03.lib.parsers import get_matrix

if TYPE_CHECKING:
    from day03.lib.classes import Matrix, PartNumber


def test_part1() -> None:
    matrix: Matrix = get_matrix(INPUT_SMALL)
    part_numbers: list[PartNumber] = matrix.get_part_numbers()
    part_numbers = matrix.filter_engine_parts(part_numbers)
    assert part1(part_numbers) == 4361


def test_part2() -> None:
    matrix: Matrix = get_matrix(INPUT_SMALL)
    part_numbers: list[PartNumber] = matrix.get_part_numbers()
    part_numbers = matrix.filter_engine_parts(part_numbers)
    assert part2(part_numbers, matrix) == 467835
