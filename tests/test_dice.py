from collections import defaultdict
from typing import Dict

import pytest

from fight_tracker.dice import Dice, Roll


def test_dice_str() -> None:
    assert str(Dice(20)) == "d20"

    assert str(3 * Dice(6)) == "3d6"


@pytest.mark.parametrize("n_sides", (4, 6, 8, 10, 12, 20))
def test_dice_int(n_sides: int) -> None:
    N_TESTS = 1000

    hist: Dict[int, int] = defaultdict(int)
    dice = Dice(n_sides)

    for _ in range(N_TESTS):
        hist[int(dice)] += 1

    assert set(hist.keys()) == set(range(1, n_sides + 1))

    for c in hist.values():
        assert c == pytest.approx(N_TESTS / n_sides, rel=0.5)


def test_roll() -> None:
    x = 2 * Dice.expectation(6) + 2

    given = Roll.outcome(x)
    assert str(given) == "9 (2d6 + 2)"
