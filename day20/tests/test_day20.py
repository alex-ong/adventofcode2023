from day20.day20 import FILE_A, FILE_B, FILE_PROD, part1, part2
from day20.lib.parsers import get_modules


def test_day20() -> None:
    modules = get_modules(FILE_A)
    assert part1(modules) == 32000000

    modules = get_modules(FILE_B)
    assert part1(modules) == 11687500


def test_part2() -> None:
    modules = get_modules(FILE_PROD)
    assert part2(modules)[0] == 252667369442479
