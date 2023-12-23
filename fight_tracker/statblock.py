from dataclasses import dataclass
from typing import Collection, Mapping

from .dice import Dice
from .mechanics.ability import AbilityModifier, Skill
from .mechanics.misc import Alignment, Size
from .mechanics.speed import Speed
from .rendering.table import BoolCell, Table
from .typing import Intable


@dataclass
class Action:
    name: str
    description: str
    category: str | None = None


@dataclass
class StatBlock:
    name: str
    nickname: str | None = None
    proficency_bonus: int | None = None
    level: int | None = None
    size: Size | None = None
    category: int | None = None
    alignment: Alignment | None = None
    armor_class: Intable | None = None
    max_hit_points: Intable | None = None
    current_hit_points: int | None = None
    speed: Speed | None = None
    ability_modifiers: Collection[AbilityModifier] | None = None
    skills: Collection[Skill] | None = None
    passive_perception: int | None = None
    senses: Collection[str] | None = None
    languages: Collection[str] | None = None
    challenge_rating: str | None = None
    abilities: Mapping[str, str] | None = None
    actions: Collection[str] | None = None

    @classmethod
    def compute_armor_class(
        cls, dice_sides: int, n_dices: int, cons_bonus: int
    ) -> Intable:
        return n_dices * Dice(dice_sides, rng="expectation") + n_dices * cons_bonus

    # def __render__(self):
    #     if self.nickname is None:
    #         title = self.name
    #     else:
    #         title = f"{self.nickname} ({self.name})"

    #     alignment_str = self.alignment.name if self.alignment else None
    #     return Div(
    #         h1(title),
    #         ", ".join([x for x in (self.size, alignment_str) if x is not None]),
    #         Description(dict())
    #     )
