from typing import List

from ..concept import Concept
from .speed import Distance


class Sense(Concept):
    pass


class DistanceBasedSense(Sense):
    def __init__(self, distance: int | Distance) -> None:
        super().__init__()
        if not isinstance(distance, Distance):
            distance = Distance(distance)
        self.distance = distance

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.distance!r})"

    def __render__(self) -> List:
        return [self.__class__.__name__, self.distance]

    def short_repr(self):
        return f"{self.__class__.__name__} {self.distance}"


class Darkvision(DistanceBasedSense):
    def long_repr(self):
        return (
            f"Up to {self.distance}, this creature can see in the see in dim "
            "light within as if it were bright light, and in darkness as if it "
            "were dim light. It cannot discern color in darkness, only shades "
            "of gray."
        )


class Tremorsense(DistanceBasedSense):
    def long_repr(self):
        return (
            f"Up to {self.distance}, this creature can detect and pinpoint the "
            "origin of vibrations, provided that this creature and the source "
            "of the vibrations are in contact with the same ground or "
            "substance. Tremorsense can't be used to detect flying or "
            "incorporeal creatures."
        )


class Truesight(DistanceBasedSense):
    def long_repr(self):
        return (
            f"Up to {self.distance}, this creature can see in normal and "
            "magical darkness, see invisible creatures and objects, "
            "automatically detect visual illusions and succeed on saving "
            "throws against them, and perceive the original form of a "
            "shapechanger or a creature that is transformed by magic. "
            "Furthermore, this creature can see into the Ethereal Plane "
            "within the same range."
        )


class Blindsight(DistanceBasedSense):
    def long_repr(self):
        return (
            f"Up to {self.distance}, this creature can perceive its "
            "surroundings without relying on sight"
        )
