"""day7 solution"""
from collections import defaultdict
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Hand:
    """Simple hand class, uses cards_inted and of_a_kind for sorting"""

    cards: str
    bet: int

    cards_inted: list[int] = field(init=False, repr=False)
    of_a_kind: list[int] = field(init=False)
    CARD_MAPPING: ClassVar[str] = "23456789TJQKA"

    def __post_init__(self):
        """convert cards to ints"""
        self.cards_inted = [self.CARD_MAPPING.index(card) for card in self.cards]
        self.bet = int(self.bet)
        self.of_a_kind = self.calculate_oak()

    def calculate_oak(self):
        """Figure out card sets"""
        card_sets = defaultdict(int)
        for card in self.cards:
            card_sets[card] += 1
        return sorted(card_sets.values(), reverse=True)

    def __lt__(self, other):
        """Less than comparator function"""
        # compare our sets
        for ours, theirs in zip(self.of_a_kind, other.of_a_kind):
            if ours != theirs:
                return ours < theirs
        # compare our individual cards
        return self.cards_inted < other.cards_inted  # int lists easy to compare


class HandPart2(Hand):
    """Part two; implements joker rule"""

    CARD_MAPPING = "J23456789TQKA"  # new card ordering

    # override
    def calculate_oak(self):
        """
        Figure out card sets;
        jokers will be added to the biggest card set
        """

        card_sets = defaultdict(int)
        for card in self.cards:
            card_sets[card] += 1

        jokers = card_sets.pop("J", 0)
        if len(card_sets) == 0:
            return [jokers]

        of_a_kind = sorted(card_sets.values(), reverse=True)
        of_a_kind[0] += jokers
        return of_a_kind


def parse_lines(cls):
    """open input file and parse into hand structures"""

    with open("input.txt", "r", encoding="utf8") as file:
        # wow super cool list comprehension thingo i'm so cool
        results = [cls(*line.split()) for line in file]
    return results


def calculate_hands(cls):
    """generates class `cls` then calculates points"""
    hands = sorted(parse_lines(cls))

    score = 0
    for rank, hand in enumerate(hands):
        score += (rank + 1) * hand.bet
    print(score)


def main():
    """main func"""
    # Q1
    calculate_hands(Hand)

    # Q2
    calculate_hands(HandPart2)


if __name__ == "__main__":
    main()
