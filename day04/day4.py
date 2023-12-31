"""Day 4 solution."""

INPUT = "day04/input.txt"
INPUT_SMALL = "day04/input-small.txt"


def split_numbers(string: str) -> set[int]:
    """Splits a list of string'ed numbers into a set.

    E.g: `` 39 40 41 42 `` -> ``set(39,40,41,42)``

    Args:
        string (str): a list of string'ed numbers

    Returns:
        set[int]: a set of integers
    """
    string = string.strip()

    return {int(number) for number in string.split()}


class Card:
    """a card with winners and numbers we own."""

    id: int = 0
    winners: set[int]
    have: set[int]

    def __init__(self, input_string: str):
        """Construct a Card from a simple input string.

        Args:
            input_string (str): ``Card 1: 41 48 | 83 86``
        """
        line = input_string.strip()
        card_id_str, numbers_str = line.split(":")
        winners_str, have_str = numbers_str.split("|")

        self.id = int(card_id_str.split()[1])
        self.winners = split_numbers(winners_str)
        self.have = split_numbers(have_str)

    def get_points(self) -> int:
        """Returns how many points the card is worth.

        Returns:
            int: 0 for no match, otherwise 2^(matches-1)
        """
        matches = self.get_matches()

        if matches == 0:
            points = 0
        else:
            points = 2 ** (matches - 1)

        return points

    def get_matches(self) -> int:
        """Returns how many winners intersect with what we have."""
        intersection = self.winners.intersection(self.have)
        return len(intersection)


class Inventory:
    """Total inventory of cards based on Question2 accumulation."""

    # mapping of card to how many more cards it makes
    memoized: dict[int, int]
    all_cards: list[Card]

    def __init__(self, all_cards: list[Card]):
        """An inventory from a list of cards.

        Args:
            all_cards (list[Card]): list of original cards
        """
        self.all_cards = all_cards
        self.memoized = self.calculate_mappings()

    def calculate_mappings(self) -> dict[int, int]:
        """Returns map of card_id -> cards owned."""
        mappings = {}
        reversed_cards = self.all_cards[::-1]
        for card in reversed_cards:
            matches = card.get_matches()
            if matches == 0:
                mappings[card.id] = 1
            else:
                total = sum(mappings[card.id + i] for i in range(1, matches + 1))
                mappings[card.id] = 1 + total
        return mappings

    def total_cards(self) -> int:
        """Return total cards in inventory."""
        return sum(self.memoized.values())


def grab_data(filename: str) -> list[Card]:
    """Converts file into wellformed cards."""
    with open(filename, "r", encoding="utf8") as file:
        result = [Card(line) for line in file]
    return result


def part1(cards: list[Card]) -> int:
    """Return sum of points for each card in list."""
    return sum(card.get_points() for card in cards)


def part2(cards: list[Card]) -> int:
    """Return total number of cards in our inventory."""
    inventory: Inventory = Inventory(cards)
    return inventory.total_cards()


def main() -> None:
    """Loads input file then runs part1 and part2."""
    cards: list[Card] = grab_data(INPUT)
    # Q1
    print(part1(cards))
    # Q2
    print(part2(cards))


if __name__ == "__main__":
    main()
