from __future__ import annotations

from copy import copy
from enum import Enum


class Unit(Enum):
    METERS = "m"
    FEET = "ft"
    SQUARES = "sq"

    def feet2meters(self, feet):
        return feet * 0.3048

    def feet2squares(self, feet):
        return feet / 5.0

    def squares2feet(self, sq):
        return sq * 5.0

    def meters2feet(self, meters):
        return meters / 0.3048


class Distance:
    def __init__(self, distance: float, unit: Unit = Unit.FEET):
        self.unit = unit

        if unit == Unit.METERS:
            distance = unit.meters2feet(distance)
        elif unit == Unit.SQUARES:
            distance = unit.squares2feet(distance)

        self.in_feet = distance

    @property
    def feet(self):
        return self.in_feet

    @property
    def meters(self):
        return self.unit.feet2meters(self.in_feet)

    @property
    def square_grid(self):
        return self.unit.feet2squares(self.in_feet)

    @property
    def in_unit(self) -> float:
        if self.unit == Unit.SQUARES:
            dist = self.square_grid
        elif self.unit == Unit.METERS:
            dist = self.meters
        else:
            dist = self.feet
        return dist

    def __str__(self):
        return f"{self.in_unit} {self.unit.value}"

    def as_unit(self, unit: Unit):
        clone = copy(self)
        clone.unit = unit
        return clone


class Speed(Distance):
    def __init__(self, speed, unit=Unit.FEET):
        super().__init__(speed, unit)

    @property
    def prefix(self):
        return ""

    def __str__(self):
        prefix = self.prefix
        if len(prefix) > 0:
            prefix += " "

        return f"{prefix}{super().__str__()}"


class FlyingSpeed(Speed):
    @property
    def prefix(self):
        return "fly"


class SwimmingSpeed(Speed):
    @property
    def prefix(self):
        return "swim"


class MultiSpeed(Speed):
    def __init__(
        self,
        base_speed: Speed,
        *other_speeds: Speed,
    ) -> None:
        super().__init__(base_speed, unit=base_speed.unit)
        self.speeds = tuple([base_speed] + list(other_speeds))

    def __str__(self):
        return ", ".join(str(x) for x in self.speeds)

    def as_unit(self, unit: Unit):
        clone = copy(self)
        speeds = [s.as_unit(unit) for s in self.speeds]
        clone.speeds = tuple(speeds)
        return clone


class Range(Distance):
    def __init__(
        self,
        short_range,
        long_range: float | None = None,
        unit=Unit.FEET,
    ):
        super().__init__(short_range, unit)
        if long_range is None:
            self.long_range: Distance | None = None
        else:
            self.long_range = Distance(long_range, unit)

    def as_unit(self, unit: Unit):
        clone = super().as_unit(unit)
        if self.long_range:
            clone.long_range = self.long_range.as_unit(unit)
        return clone

    def __str__(self):
        if self.long_range is None:
            return super().__str__()
        return f"{self.in_unit}/{self.long_range.in_unit} {self.unit.value}"
