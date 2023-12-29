"""day9 solution"""

from dataclasses import dataclass
from typing import Callable

INPUT = "day09/input.txt"
INPUT_SMALL = "day09/input-small.txt"


@dataclass
class ValueArray:
    sub_arrays: list[list[int]]

    def __post_init__(self) -> None:
        """Creates sub arrays"""
        current: list[int] = self.sub_arrays[0]
        while set(current) != {0}:
            current = interpolate(current)
            self.sub_arrays.append(current)

    def generic_extrapolate(
        self,
        add_to_array: Callable[[list[int], int], None],
        calc_value: Callable[[list[int], list[int]], int],
    ) -> None:
        """Generic extrapolation"""
        for i in range(-1, -len(self.sub_arrays) - 1, -1):
            array: list[int] = self.sub_arrays[i]
            if i == -1:
                add_to_array(array, 0)
            else:
                array_below: list[int] = self.sub_arrays[i + 1]
                new_value = calc_value(array, array_below)
                add_to_array(array, new_value)

    def extrapolate_right(self) -> None:
        """Extrapolates to the right"""

        def add_to_array(array: list[int], value: int) -> None:
            array.append(value)

        def calculate_value(array: list[int], array_below: list[int]) -> int:
            return array[-1] + array_below[-1]

        self.generic_extrapolate(add_to_array, calculate_value)

    def extrapolate_left(self) -> None:
        """Extrapolates to the left"""

        def add_to_array(array: list[int], value: int) -> None:
            array.insert(0, value)

        def calculate_value(array: list[int], array_below: list[int]) -> int:
            return array[0] - array_below[0]

        self.generic_extrapolate(add_to_array, calculate_value)


def get_input(path: str) -> list[ValueArray]:
    """Turns inputs into nice ValueArrays"""
    result = []
    with open(path, "r", encoding="utf8") as file:
        for line in file:
            values = ValueArray([[int(item) for item in line.split()]])
            result.append(values)
    return result


def interpolate(values: list[int]) -> list[int]:
    """Converts 3 3 3 3
           to 0 0 0
    Converts 1 2 3 4
           to 1 1 1
    """
    result = [values[i + 1] - values[i] for i in range(len(values) - 1)]

    return result


def part1(inputs: list[ValueArray]) -> int:
    for input in inputs:
        input.extrapolate_right()
    return sum(input.sub_arrays[0][-1] for input in inputs)


def part2(inputs: list[ValueArray]) -> int:
    for input in inputs:
        input.extrapolate_left()

    return sum(input.sub_arrays[0][0] for input in inputs)


def main() -> None:
    """Main function"""
    inputs = get_input(INPUT)

    # q1
    print(part1(inputs))

    # q2
    print(part2(inputs))


if __name__ == "__main__":
    main()
