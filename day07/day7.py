"""day7 solution"""
from collections import defaultdict
from dataclasses import dataclass, field
from functools import total_ordering
from typing import Any, ClassVar, Self

INPUT = "day07/input.txt"
INPUT_SMALL = "day07/input-small.txt"


@total_ordering
@dataclass(eq=False)
class Hand:
    """Simple hand class, uses cards_inted and of_a_kind for sorting"""

    cards: str
    bet: int

    cards_inted: list[int] = field(init=False, repr=False)
    of_a_kind: list[int] = field(init=False)
    CARD_MAPPING: ClassVar[str] = "23456789TJQKA"

    def __post_init__(self) -> None:
        """Convert cards to ints"""
        self.cards_inted = [self.CARD_MAPPING.index(card) for card in self.cards]
        self.bet = int(self.bet)
        self.of_a_kind = self.calculate_of_a_kind()

    def calculate_of_a_kind(self) -> list[int]:
        """Figure out card sets"""
        card_sets: dict[str, int] = defaultdict(int)
        for card in self.cards:
            card_sets[card] += 1
        return sorted(card_sets.values(), reverse=True)

    def __lt__(self, other: Self) -> Any:
        """Less than comparator function"""
        if not isinstance(other, Hand):
            raise ValueError("using __lt__ on non identical class")
        # compare our sets
        for ours, theirs in zip(self.of_a_kind, other.of_a_kind):
            if ours != theirs:
                return ours < theirs
        # compare our individual cards
        return self.cards_inted < other.cards_inted  # int lists easy to compare

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            raise ValueError("using __lt__ on non identical class")
        return self.cards_inted == other.cards_inted


class HandPart2(Hand):
    """Part two; implements joker rule"""

    CARD_MAPPING = "J23456789TQKA"  # new card ordering

    # override
    def calculate_of_a_kind(self) -> list[int]:
        """Figure out card sets;
        jokers will be added to the biggest card set
        """
        card_sets: dict[str, int] = defaultdict(int)
        for card in self.cards:
            card_sets[card] += 1

        jokers = card_sets.pop("J", 0)
        if len(card_sets) == 0:
            return [jokers]

        of_a_kind = sorted(card_sets.values(), reverse=True)
        of_a_kind[0] += jokers
        return of_a_kind


def parse_lines(cls: type, path: str) -> list[Hand]:
    """Open input file and parse into hand structures"""
    with open(path, "r", encoding="utf8") as file:
        # wow super cool list comprehension thingo i'm so cool
        results = [cls(*line.split()) for line in file]
    return results


def calculate_hands(cls: type, input_path: str) -> int:
    """Generates class `cls` then calculates points"""
    hands = sorted(parse_lines(cls, input_path))

    score = 0
    for rank, hand in enumerate(hands):
        score += (rank + 1) * hand.bet
    return score


def main() -> None:
    """Main func"""
    # Q1
    print(calculate_hands(Hand, INPUT))

    # Q2
    print(calculate_hands(HandPart2, INPUT))


if __name__ == "__main__":
    main()
