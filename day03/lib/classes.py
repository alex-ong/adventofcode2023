import re
from dataclasses import dataclass

NON_PART = "123456789."
NUMBER_REGEX = r"\d+"


@dataclass
class PartNumber:
    col: int
    row: int
    length: int
    value: int

    def touching(self, col: int, row: int, row_size: int) -> bool:
        """Returns if a given coordinate is touching this PartNumber"""
        start_x = max(0, self.col - 1)
        end_x = min(self.end_index, row_size)

        if not start_x <= col <= end_x:
            return False
        if not self.row - 1 <= row <= self.row + 1:
            return False
        return True

    @property
    def end_index(self) -> int:
        return self.col + self.length


@dataclass
class Gear:
    col: int
    row: int

    part_numbers: list[PartNumber] | None = None

    @property
    def gear_ratio(self) -> int:
        """If we have exactly two parts, returns the gear ratio"""
        if self.part_numbers is None:
            raise ValueError("self.part_numbers not initialized")
        if len(self.part_numbers) == 2:
            return self.part_numbers[0].value * self.part_numbers[1].value
        return 0  # or None..


@dataclass
class Matrix:
    data: list[str]

    @property
    def row_size(self) -> int:
        return len(self.data[0])

    @property
    def row_count(self) -> int:
        return len(self.data)

    def get_part_numbers(self) -> list[PartNumber]:
        """Retrieve numbered words like 456 from the matrix"""
        results = []

        for row, line in enumerate(self.data):
            matches = re.finditer(NUMBER_REGEX, line)
            for match in matches:
                start, end = match.start(), match.end()
                value = int(line[start:end])
                part_number = PartNumber(
                    row=row, col=start, length=end - start, value=value
                )
                results.append(part_number)
        return results

    @staticmethod
    def is_engine_part_row(row: str) -> bool:
        """Returns if there is an engine part in this row"""
        return any(char not in NON_PART for char in row)

    def is_engine_part(self, part_number: PartNumber) -> bool:
        """Return whether a part_number is an engine part by looking at its surroundings"""
        start_x = max(0, part_number.col - 1)
        end_x = min(part_number.end_index + 1, self.row_size)

        if (
            part_number.row >= 1
            and self.is_engine_part_row(  # row above
                self.data[part_number.row - 1][start_x:end_x]
            )
        ):
            return True
        if (  # row below
            part_number.row < self.row_count - 1
            and self.is_engine_part_row(self.data[part_number.row + 1][start_x:end_x])
        ):
            return True

        # left one
        if self.data[part_number.row][start_x] not in NON_PART:
            return True

        # right one
        if self.data[part_number.row][end_x - 1] not in NON_PART:
            return True

        return False

    def get_gears(self, part_numbers: list[PartNumber]) -> list[Gear]:
        """Retrieve gears from the matrix"""
        results = []
        for row, line in enumerate(self.data):
            for col, char in enumerate(line):
                if char == "*":
                    gear = Gear(col=col, row=row)
                    gear.part_numbers = self.find_gear_parts(gear, part_numbers)
                    results.append(gear)
        return results

    def find_gear_parts(
        self, gear: Gear, part_numbers: list[PartNumber]
    ) -> list[PartNumber]:
        """Returns a list of part_numbers that are touching a given gear"""
        result = []
        for part_number in part_numbers:
            if part_number.touching(gear.col, gear.row, self.row_size):
                result.append(part_number)
        return result

    def filter_engine_parts(self, part_numbers: list[PartNumber]) -> list[PartNumber]:
        """Return the legit part numbers"""
        return list(filter(self.is_engine_part, part_numbers))
