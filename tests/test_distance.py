import pytest

from fight_tracker.mechanics.speed import (
    FlyingSpeed,
    MultiSpeed,
    Range,
    Speed,
    SwimmingSpeed,
    Unit,
)


def test_speed() -> None:
    s = Speed(30)
    assert s.in_unit == 30
    assert s.feet == 30
    assert s.square_grid == pytest.approx(6.0)

    assert str(s) == "30 ft"

    s2 = s.as_unit(Unit.SQUARES)
    assert s2.in_unit == pytest.approx(6.0)
    assert s2.feet == pytest.approx(30)
    assert str(s2) == "6 sq"


def test_multispeed() -> None:
    s = MultiSpeed(
        Speed(30),
        FlyingSpeed(30),
        SwimmingSpeed(15),
    )

    assert str(s) == "30 ft, fly 30 ft, swim 15 ft"


def test_range() -> None:
    r = Range(100, 400)
    assert str(r) == "100/400 ft"
    assert str(r.as_unit(Unit.SQUARES)) == "20/80 sq"
