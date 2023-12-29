"""tests for day07."""
import pytest

from day07.day7 import INPUT_SMALL, Hand, HandPart2, calculate_hands, parse_lines


def test_calculate_hands() -> None:
    """Test calculating hands."""
    assert calculate_hands(Hand, INPUT_SMALL) == 6440
    assert calculate_hands(HandPart2, INPUT_SMALL) == 5905


def test_parser() -> None:
    """Test the input parsing code."""
    hands: list[Hand] = parse_lines(Hand, INPUT_SMALL)
    assert len(hands) == 5
    assert hands[0].cards == "32T3K"
    assert hands[-1].cards == "QQQJA"
    assert hands[0] == Hand("32T3K", 765)


def test_hand() -> None:
    """Test `Hand` class."""
    hand1 = Hand("KK677", 0)
    hand2 = Hand("KTJJT", 0)
    hand3 = Hand("KK677", 0)
    assert hand2 < hand1
    assert hand1 > hand2
    assert hand1 == hand3

    # mypy actually stops us from doing `hand1 < 1`
    # So we disable it so we can test our raise,
    # in case a dev decides to do the comparison
    with pytest.raises(ValueError):
        hand1 < 1  # type: ignore[operator]

    # here we don't need to disable it, since ruff
    # tells us to use __eq__(self, other:object) -> bool:
    # This means we do expect people to use hand1 == 6 and
    # we want to throw that error
    with pytest.raises(ValueError):
        hand1 == 6

    data = [
        ("32T3K", 765),
        ("T55J5", 684),
        ("KK677", 28),
        ("KTJJT", 220),
        ("QQQJA", 483),
        ("JJJJJ", 483),
    ]

    hands = (HandPart2(cards, bet) for cards, bet in data)
    oaks = [hand.calculate_of_a_kind() for hand in hands]
    assert [oak[0] for oak in oaks] == [2, 4, 2, 4, 4, 5]
