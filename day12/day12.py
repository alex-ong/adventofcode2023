"""day12 solution"""
from dataclasses import dataclass, field

INPUT = "day12/input.txt"
INPUT_SMALL = "day12/input-small.txt"


@dataclass
class State:
    items: str
    broken_springs: list[int]

    def valid(self) -> int:
        """Returns true IFF we are completed without errors
        """
        if len(self.items) == 0 and len(self.broken_springs) == 0:
            return 1
        return 0

    def __getitem__(self, index_or_slice: slice | int) -> str:
        # slice access
        if isinstance(index_or_slice, slice):
            _slice = index_or_slice
            return self.items[_slice.start : _slice.stop : _slice.step]
        # index access
        index: int = index_or_slice
        if index >= len(self.items):
            return "."
        return self.items[index]

    def __hash__(self) -> int:
        return hash(str(self.items) + ":" + str(self.broken_springs))


@dataclass
class SpringLine:
    """springline class"""

    items: str
    broken_springs: list[int]
    big_cache: dict[State, int] = field(init=False, repr=False, default_factory=dict)

    def unfold(self) -> "SpringLine":
        """Makes it bigger"""
        return SpringLine("?".join([self.items] * 5), self.broken_springs * 5)

    def calculate(self) -> int:
        """Brute force with backtracking lets go..."""
        first_state = State(self.items[:], self.broken_springs[:])
        return self.calculate_recursive(first_state)

    def set_and_return(self, state: State, value: int) -> int:
        """Sets and returns in one line"""
        self.big_cache[state] = value
        return value

    def calculate_recursive(self, state: State) -> int:
        """Recursive with memoization
        1. memoized
        2. state.empty -> return if we are valid
        3. state[0] == "." chop it and continue
        4. state[0] == "#". get next number, and "enforce" it, chopping things. If anything is wrong, fail
        """
        if state in self.big_cache:
            return self.big_cache[state]
        if len(state.items) == 0:
            return self.set_and_return(state, state.valid())
        if state[0] == ".":
            dot_state = State(state.items[1:], state.broken_springs[:])
            return self.set_and_return(state, self.calculate_recursive(dot_state))
        if state[0] == "#":
            if len(state.broken_springs) == 0:
                return self.set_and_return(state, 0)

            # commit to the state or die trying
            broken = state.broken_springs[0]
            items = state[:broken]

            if len(items) < broken:  # at end of array and not enough elements
                return self.set_and_return(state, 0)
            if items.count(".") > 0:  # only accept # and ?
                return self.set_and_return(state, 0)
            if state[broken] == "#":  # check right hand side, needs to be ? or .
                return self.set_and_return(state, 0)

            state = State(state[broken + 1 :], state.broken_springs[1:])
            return self.set_and_return(state, self.calculate_recursive(state))
        if state[0] == "?":
            hash_state = State("#" + state.items[1:], state.broken_springs[:])
            dot_state = State("." + state.items[1:], state.broken_springs[:])

            result = self.calculate_recursive(hash_state)
            result += self.calculate_recursive(dot_state)
            return self.set_and_return(state, result)

        raise AssertionError("First char not in `.#?` and list not empty")


def get_input(path: str) -> list[SpringLine]:
    """Returns list of SpringLines from input file"""
    result = []
    with open(path, "r", encoding="utf8") as file:
        for line in file:
            items, broken_csv = line.split()
            int_springs = [int(item) for item in broken_csv.split(",")]
            spring_line = SpringLine(items, int_springs)
            result.append(spring_line)
    return result


def calculate_sum(spring_lines: list[SpringLine]) -> int:
    """Calculates every spring line and then adds the totals"""
    return sum(spring_line.calculate() for spring_line in spring_lines)


def main() -> None:
    """Main function"""
    spring_lines = get_input(INPUT)
    # q1
    print(calculate_sum(spring_lines))
    # q2
    spring_lines_big = [spring_line.unfold() for spring_line in spring_lines]
    print(calculate_sum(spring_lines_big))


if __name__ == "__main__":
    main()
