"""
Day 3 implementation
"""

from typing import TYPE_CHECKING

from day03.classes import Gear, Matrix

if TYPE_CHECKING:
    from day03.classes import PartNumber


def get_data() -> Matrix:
    """Convert text file to matrix"""
    with open("input.txt", "r", encoding="utf8") as file:
        data = file.readlines()
        data = [line.strip() for line in data]
    return Matrix(data=data)


def main() -> None:
    matrix = get_data()
    part_numbers = matrix.get_part_numbers()

    def part_filter(part_number: "PartNumber") -> bool:
        return matrix.is_engine_part(part_number)

    part_numbers = list(filter(part_filter, part_numbers))

    # q1
    print(sum([part_number.value for part_number in part_numbers]))

    # q2
    gears: list[Gear] = matrix.get_gears(part_numbers)
    print(sum(gear.gear_ratio for gear in gears))


if __name__ == "__main__":
    main()
