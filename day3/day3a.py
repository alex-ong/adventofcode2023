"""
Day 3 implementation
"""
import re
from dataclasses import dataclass

NON_PART = "123456789."


@dataclass
class Matrix:
    data: list[str]

    @property
    def row_size(self) -> int:
        return len(self.data[0])

    @property
    def row_count(self) -> int:
        return len(self.data)


@dataclass
class Word:
    col: int
    row: int
    length: int
    value: int

    def touching(self, col, row, row_size):
        start_x = max(0, self.col - 1)
        end_x = min(self.end_index, row_size)

        if not start_x <= col <= end_x:
            return False
        if not self.row - 1 <= row <= self.row + 1:
            return False
        return True

    @property
    def end_index(self):
        return self.col + self.length

    def is_engine_part(self, matrix):
        """row above"""
        row_size, num_rows = matrix.row_size, matrix.row_count
        start_x = max(0, self.col - 1)
        end_x = min(self.end_index + 1, row_size)
        data = matrix.data
        if self.row >= 1:  # row above
            for char in data[self.row - 1][start_x:end_x]:
                if char not in NON_PART:
                    return True
        if self.row < num_rows - 1:  # row below
            for char in data[self.row + 1][start_x:end_x]:
                if char not in NON_PART:
                    return True
        if self.col >= 1:  # left one
            if data[self.row][self.col - 1] not in NON_PART:
                return True
        if self.end_index < row_size - 1:  # right one
            if data[self.row][self.end_index] not in NON_PART:
                return True

        return False


@dataclass
class Gear:
    col: int
    row: int

    words: list[Word] = None

    @property
    def gear_ratio(self):
        if self.words is None:
            raise ValueError("self.words not intialized")
        if len(self.words) == 2:
            return self.words[0].value * self.words[1].value
        return 0  # or None..

    def find_words(self, words: list[Word], matrix):
        if self.words is not None:
            return self.words
        result = []
        for word in words:
            if word.touching(self.col, self.row, matrix.row_size):
                result.append(word)
        self.words = result
        return result


NUMBER_REGEX = r"\d+"


def get_words(matrix: Matrix):
    results = []

    for row, line in enumerate(matrix.data):
        matches = re.finditer(NUMBER_REGEX, line)
        for match in matches:
            start, end = match.start(), match.end()
            value = int(line[start:end])
            word = Word(row=row, col=start, length=end - start, value=value)
            results.append(word)
    return results


def get_gears(matrix: Matrix):
    results = []
    for row, line in enumerate(matrix.data):
        for col, char in enumerate(line):
            if char == "*":
                gear = Gear(col=col, row=row)
                results.append(gear)
    return results


def get_data() -> Matrix:
    with open("data.txt", "r", encoding="utf8") as file:
        data = file.readlines()
        data = [line.strip() for line in data]
    return Matrix(data=data)


def main():
    matrix = get_data()
    words = get_words(matrix)
    part_filter = lambda x: x.is_engine_part(matrix)
    words = list(filter(part_filter, words))
    # q1
    print(sum([word.value for word in words]))
    # q2
    gears = get_gears(matrix)

    for gear in gears:
        gear.find_words(words, matrix)
        if len(gear.words) != 2:
            print(gear)

    print(sum(gear.gear_ratio for gear in gears))


if __name__ == "__main__":
    main()
