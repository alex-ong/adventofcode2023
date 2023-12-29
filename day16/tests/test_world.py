"""Test World class."""
from typing import TYPE_CHECKING

from day16.day16 import INPUT_SMALL
from day16.lib.direction import Direction
from day16.lib.laser import Laser
from day16.lib.parsers import get_input

if TYPE_CHECKING:
    from day16.lib.world import SolvedWorld, World


def test_world() -> None:
    """Test ``World`` class."""
    world: World = get_input(INPUT_SMALL)
    start_laser: Laser = Laser(0, 0, Direction.EAST)
    solved_world: SolvedWorld = world.solve(start_laser)

    print(solved_world)
    assert str(solved_world) == "\n".join(
        [
            "1211110000",
            "0100010000",
            "0100011111",
            "0100011000",
            "0100011000",
            "0100011000",
            "0100122100",
            "1211111100",
            "0111121100",
            "0100010100",
        ]
    )
