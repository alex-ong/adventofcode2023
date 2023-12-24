"""
Day 3 implementation
"""


from day03.lib.classes import Gear, Matrix, PartNumber
from day03.lib.parsers import get_matrix

INPUT = "day03/input.txt"
INPUT_SMALL = "day03/input-small.txt"


def part1(part_numbers: list[PartNumber]) -> int:
    return sum([part_number.value for part_number in part_numbers])


def part2(part_numbers: list[PartNumber], matrix: Matrix) -> int:
    gears: list[Gear] = matrix.get_gears(part_numbers)
    return sum(gear.gear_ratio for gear in gears)


def main() -> None:
    matrix: Matrix = get_matrix(INPUT)
    part_numbers: list["PartNumber"] = matrix.get_part_numbers()
    part_numbers = matrix.filter_engine_parts(part_numbers)

    # q1
    print(part1(part_numbers))

    # q2
    print(part2(part_numbers, matrix))


if __name__ == "__main__":
    main()
