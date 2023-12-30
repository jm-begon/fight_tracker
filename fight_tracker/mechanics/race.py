from dataclasses import dataclass

from .misc import Size
from .speed import Speed


@dataclass
class Race:
    subtype: str
    size: Size
    speed: Speed

    @property
    def type(self) -> str:
        return f"Humanoid ({self.subtype})"


HUMAN = Race(
    "Human",
    Size.MEDIUM,
    Speed(30),
)

GNOME = Race(
    "Gnome",
    Size.SMALL,
    Speed(25),
)
