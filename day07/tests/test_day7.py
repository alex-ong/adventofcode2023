from day07.day7 import INPUT_SMALL, Hand, HandPart2, calculate_hands, parse_lines


def test_calculate_hands() -> None:
    assert calculate_hands(Hand, INPUT_SMALL) == 6440
    assert calculate_hands(HandPart2, INPUT_SMALL) == 5905


def test_parser() -> None:
    hands: list[Hand] = parse_lines(Hand, INPUT_SMALL)
    assert len(hands) == 5
    assert hands[0].cards == "32T3K"
    assert hands[-1].cards == "QQQJA"
    assert hands[0] == Hand("32T3K", 765)


def test_hand() -> None:
    hand1 = Hand("KK677", 0)
    hand2 = Hand("KTJJT", 0)
    hand3 = Hand("KK677", 0)
    assert hand2 < hand1
    assert hand1 > hand2
    assert hand1 == hand3
