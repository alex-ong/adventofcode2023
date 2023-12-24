from day04.day4 import INPUT_SMALL, Card, Inventory, grab_data, split_numbers


def test_split_numbers() -> None:
    assert split_numbers("6 7 8 9 10") == {6, 7, 8, 9, 10}
    assert split_numbers("") == set()
    assert split_numbers("6 6 6 6 6") == {6}


def test_grab_data() -> None:
    cards: list[Card] = grab_data(INPUT_SMALL)
    assert len(cards) == 6
    assert cards[0].id == 1 and cards[-1].id == 6


def test_card() -> None:
    card = Card("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n")
    assert card.get_points() == 8
    assert card.get_matches() == 4


def test_inventory() -> None:
    cards: list[Card] = grab_data(INPUT_SMALL)
    inventory: Inventory = Inventory(cards)
    assert inventory.total_cards() == 30
