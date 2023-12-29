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


class Speed:
    def __init__(self, speed, unit=Unit.FEET):
        self.unit = unit

        if unit == Unit.METERS:
            speed = unit.meters2feet(speed)
        elif unit == Unit.SQUARES:
            speed = unit.squares2feet(speed)

        self.in_feet = speed

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
    def prefix(self):
        return ""

    def __str__(self):
        prefix = self.prefix
        if len(prefix) > 0:
            prefix += " "

        if self.unit == Unit.SQUARES:
            speed = self.square_grid
        elif self.unit == Unit.METERS:
            speed = self.meters
        else:
            speed = self.feet
        return f"{prefix}{speed} {self.unit.value}"

    def as_unit(self, unit: Unit) -> Speed:
        clone = copy(self)
        clone.unit = unit
        return clone


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

    def as_unit(self, unit: Unit) -> Speed:
        clone = copy(self)
        speeds = [s.as_unit(unit) for s in self.speeds]
        clone.speeds = tuple(speeds)
        return clone
