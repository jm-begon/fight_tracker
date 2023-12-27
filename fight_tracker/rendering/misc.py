from __future__ import annotations

from ..typing import Intable


class HPBar:
    @classmethod
    def create(cls, hp_max: Intable | None, hp: Intable | None = None) -> HPBar | None:
        if hp_max is None and hp is None:
            return None
        if hp is None:
            hp = hp_max
        if hp_max is None:
            hp_max = hp

        return cls(hp, hp_max)

    def __init__(self, hp, hp_max):
        self.hp = hp
        self.hp_max = hp_max

    def __str__(self):
        return f"{self.hp}/{self.hp_max}"
