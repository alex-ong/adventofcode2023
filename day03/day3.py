"""
Day 3 implementation
"""


from day03.classes import Gear, Matrix, PartNumber

INPUT = "day03/input.txt"
INPUT_SMALL = "day03/input-small.txt"


def get_data(path: str) -> Matrix:
    """Convert text file to matrix"""
    with open(path, "r", encoding="utf8") as file:
        data = file.readlines()
        data = [line.strip() for line in data]
    return Matrix(data=data)


def part1(part_numbers: list[PartNumber]) -> int:
    return sum([part_number.value for part_number in part_numbers])


def part2(part_numbers: list[PartNumber], matrix: Matrix) -> int:
    gears: list[Gear] = matrix.get_gears(part_numbers)
    return sum(gear.gear_ratio for gear in gears)


def main() -> None:
    matrix: Matrix = get_data(INPUT)
    part_numbers: list["PartNumber"] = matrix.get_part_numbers()
    part_numbers = matrix.filter_engine_parts(part_numbers)

    # q1
    print(part1(part_numbers))

    # q2
    print(part2(part_numbers, matrix))


if __name__ == "__main__":
    main()
