from dataclasses import dataclass
from enum import Enum


class Check(Enum):
    CONTINUE = 0
    SUCCESS = 1
    FAIL = 2


@dataclass
class State:
    items: list[str]
    broken_remaining: int
    current_index: int = 0

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.items[index.start : index.stop : index.step]
        if index < 0:
            return "."
        if index >= len(self.items):
            return "."
        return self.items[index]

    def __len__(self):
        return len(self.items)

    def count(self, character="?"):
        """Returns count of given character"""
        return self.items.count(character)


class HashState(State):
    def __init__(self, prev_state: State, index: int):
        self.items = prev_state.items[:index] + "#" + prev_state.items[index + 1 :]
        self.broken_remaining = prev_state.broken_remaining - 1
        self.current_index = index


class DotState(State):
    def __init__(self, prev_state: State, index: int):
        self.items = prev_state.items[:index] + "." + prev_state.items[index + 1 :]
        self.broken_remaining = prev_state.broken_remaining
        self.current_index = index


@dataclass
class SpringLine:
    """springline class"""

    items: list[str]
    broken_springs: list[int]

    def unfold(self) -> "SpringLine":
        """makes it bigger"""
        return SpringLine("?".join([self.items] * 5), self.broken_springs * 5)

    def calculate(self):
        """brute force with backtracking lets go..."""
        first_state = State(
            self.items[:], sum(self.broken_springs) - self.items.count("#")
        )
        states = [first_state]
        result = 0
        while len(states) > 0:
            state = states.pop(0)

            check: Check = self.verify(state)
            if check == Check.FAIL:
                continue
            if check == Check.SUCCESS:
                result += 1
                continue
            self.calculate_state(states, state)
        return result

    def calculate_state(self, states: list[State], state: State):
        """
        calculates a single state,
        adding to our list if we need to expand
        """

        try:  # find first ?
            index = state.items.index("?", state.current_index)
        except ValueError:
            return  # no questionmarks left. good work

        # turn the ? into both a `#`` and a `.`
        if state.count("?") < state.broken_remaining:
            return  # can't fill enough #'s so exit

        if state.broken_remaining > 0:
            state_hash = HashState(
                state,
                index,
            )
            states.append(state_hash)

        state_dot = DotState(state, index)
        states.append(state_dot)

    def verify(self, state: State) -> Check:
        all_broken = self.broken_springs
        index = 0
        broken_index = 0

        while index < len(state):
            item = state[index]
            if item == "#":
                if broken_index >= len(all_broken):
                    return Check.FAIL
                broken = all_broken[broken_index]
                consecutive = state[index : index + broken]
                if any(x == "." for x in consecutive):
                    return Check.FAIL
                if len(consecutive) != broken:  # consecutive constructor can be small
                    return Check.FAIL
                if state[index - 1] == "#" or state[index + broken] == "#":
                    return Check.FAIL
                index += broken
                broken_index += 1
            elif item == "?":
                return Check.CONTINUE
            else:
                index += 1

        if broken_index != len(all_broken):
            if state.items.count("?") == 0:
                return Check.FAIL
            return Check.CONTINUE
        if state.count("?") == 0:
            return Check.SUCCESS
        return Check.CONTINUE


def get_input() -> list[SpringLine]:
    """returns list of SpringLines from input file"""
    result = []
    with open("input.txt", "r", encoding="utf8") as file:
        for line in file:
            items, broken_csv = line.split()
            int_springs = [int(item) for item in broken_csv.split(",")]
            spring_line = SpringLine(items, int_springs)
            result.append(spring_line)
    return result


def main():
    """main function"""
    spring_lines = get_input()
    # q1
    print(sum(line.calculate() for line in spring_lines))

    big_spring_lines = [spring_line.unfold() for spring_line in spring_lines]
    print(spring_lines[0], big_spring_lines[0])
    for spring_line in big_spring_lines:
        print(spring_line.calculate())


if __name__ == "__main__":
    main()
