"""day9 solution"""

from dataclasses import dataclass
from typing import Callable


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
        """generic extrapolation"""
        for i in range(-1, -len(self.sub_arrays) - 1, -1):
            array: list[int] = self.sub_arrays[i]
            if i == -1:
                add_to_array(array, 0)
            else:
                array_below: list[int] = self.sub_arrays[i + 1]
                new_value = calc_value(array, array_below)
                add_to_array(array, new_value)

    def extrapolate_right(self) -> None:
        """extrapolates to the right"""

        def add_to_array(array: list[int], value: int) -> None:
            array.append(value)

        def calculate_value(array: list[int], array_below: list[int]) -> int:
            return array[-1] + array_below[-1]

        self.generic_extrapolate(add_to_array, calculate_value)

    def extrapolate_left(self) -> None:
        """extrapolates to the left"""

        def add_to_array(array: list[int], value: int) -> None:
            array.insert(0, value)

        def calculate_value(array: list[int], array_below: list[int]) -> int:
            return array[0] - array_below[0]

        self.generic_extrapolate(add_to_array, calculate_value)


def get_input() -> list[ValueArray]:
    """turns inputs into nice ValueArrays"""
    result = []
    with open("day09/input.txt", "r", encoding="utf8") as file:
        for line in file:
            values = ValueArray([[int(item) for item in line.split()]])
            result.append(values)
    return result


def interpolate(values: list[int]) -> list[int]:
    """
    Converts 3 3 3 3
           to 0 0 0
    Converts 1 2 3 4
           to 1 1 1
    """
    result = [values[i + 1] - values[i] for i in range(len(values) - 1)]

    return result


def main() -> None:
    """main function"""
    inputs = get_input()

    # q1
    for input in inputs:
        input.extrapolate_right()

    print(sum(input.sub_arrays[0][-1] for input in inputs))
    # q2
    for input in inputs:
        input.extrapolate_left()

    print(sum(input.sub_arrays[0][0] for input in inputs))


if __name__ == "__main__":
    main()
