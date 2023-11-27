from enum import Enum


class Unit(Enum):
    METERS = "m"
    FEET = "ft"
    SQUARES = "sq"

    def feet2meters(self, feet):
        return feet * 0.3048

    def feet2squares(self, feet):
        return feet / 5.

    def squares2feet(self, sq):
        return sq * 5.

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


class FlyingSpeed(Speed):

    @property
    def prefix(self):
        return "fly"


class SwimmingSpeed(Speed):
    @property
    def prefix(self):
        return "swim"
