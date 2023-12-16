"""
Day 4 solution
"""



def split_numbers(string):
    """
    Splits a list of string'ed numbers into a set
    E.g: ` 39 40 41 42 ` -> set(39,40,41,42)
    """
    string = string.strip()

    return {int(number) for number in string.split()}


class Card:
    id: int = 0
    winners: set[int]
    have: set[int]

    def __init__(self, input_string):
        line = input_string.strip()
        card_id_str, numbers_str = line.split(":")
        winners_str, have_str = numbers_str.split("|")

        self.id = int(card_id_str.split()[1])
        self.winners = split_numbers(winners_str)
        self.have = split_numbers(have_str)

    def get_points(self):
        """Returns how many points the card is worth"""
        matches = self.get_matches()

        if matches == 0:
            points = 0
        else:
            points = 2 ** (matches - 1)

        return points

    def get_matches(self):
        intersection = self.winners.intersection(self.have)
        return len(intersection)


class Inventory:
    # mapping of card to how many more cards it makes
    memoized: dict[int, int]

    def __init__(self, all_cards: list[Card]):
        self.all_cards = all_cards
        self.memoized = self.calculate_mappings()

    def calculate_mappings(self):
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

    def total_cards(self):
        return sum(self.memoized.values())


def grab_data(filename: str) -> list[Card]:
    """Converts file into wellformed cards"""
    with open(filename, "r", encoding="utf8") as file:
        result = [Card(line) for line in file]
    return result


def main():
    cards: list[Card] = grab_data("input.txt")
    # Q1
    total_points = sum(card.get_points() for card in cards)
    print(total_points)
    # Q2
    inventory = Inventory(cards)
    print(inventory.total_cards())


if __name__ == "__main__":
    main()
