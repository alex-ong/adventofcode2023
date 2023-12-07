from collections import defaultdict
from dataclasses import dataclass, field


def card_set_dict():
    return defaultdict(int)


card_mapping = "23456789TJQKA"


@dataclass
class Hand:
    cards: str
    bet: int

    cards_inted: list[int] = field(init=False)
    card_sets: dict[str, int] = field(default_factory=card_set_dict)
    of_a_kind: list[int] = field(init=False)

    def __post_init__(self):
        """convert cards to ints"""
        self.cards_inted = []
        for card in self.cards:
            self.cards_inted.append(card_mapping.index(card))

        self.bet = int(self.bet)

        """Figure out card sets"""
        for card in self.cards:
            self.card_sets[card] += 1
        self.of_a_kind = sorted(self.card_sets.values(), reverse=True)

    def __lt__(self, other):
        for index in range(len(self.of_a_kind)):
            ours, theirs = self.of_a_kind[index], other.of_a_kind[index]
            if ours < theirs:
                return True
            elif ours > theirs:
                return False
        return self.cards_inted < other.cards_inted

    def __str__(self):
        return f"{self.of_a_kind}, [{self.cards} | {self.cards_inted}], {self.bet}"


def parse_lines():
    """open input file and parse into hand structures"""

    with open("input.txt", "r", encoding="utf8") as file:
        # wow super cool list comprehension thingo i'm so cool
        results = [Hand(*line.split()) for line in file]
    return results


def main():
    """main func"""
    hands = parse_lines()
    hands.sort()

    for hand in hands:
        print(hand)

    total = 0
    for rank, hand in enumerate(hands):
        total += (rank + 1) * hand.bet
    print(total)


if __name__ == "__main__":
    main()
