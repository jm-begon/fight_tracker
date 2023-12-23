from __future__ import annotations

from abc import ABCMeta
from dataclasses import dataclass
from enum import Enum

from ..arithmetic import DescriptiveInt


class Ability(Enum):
    STR = "strength"
    DEX = "dexterity"
    CON = "constitution"
    INT = "intelligence"
    WIS = "wisdom"
    CHA = "charisma"

    @classmethod
    def __getitem__(cls, item):
        if item is None:
            return None

        if isinstance(item, cls):
            return item
        for ability in cls:
            if item == ability.value or ability.name:
                return ability

        return None


@dataclass
class AbilityModifier(DescriptiveInt):
    ability: Ability
    value: int

    @classmethod
    def from_score(cls, ability: Ability, score: int) -> AbilityModifier:
        value = (score - 10) // 2
        return cls(ability, value)

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return f"{self.value} ({self.ability.name})"


class Skill(metaclass=ABCMeta):
    def __init__(
        self, ability: Ability, raw_score: int, proficiency_bonus: int = 0
    ) -> None:
        self.ability = ability
        self.raw_score = raw_score
        self.proficiency_bonus = proficiency_bonus

    def __int__(self) -> int:
        return self.raw_score + self.proficiency_bonus


class Athletics(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.STR, raw_score, proficiency_bonus)


class Acrobatics(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.DEX, raw_score, proficiency_bonus)


class SleightofHand(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.DEX, raw_score, proficiency_bonus)


class Arcana(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.INT, raw_score, proficiency_bonus)


class History(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.INT, raw_score, proficiency_bonus)


class Investigation(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.INT, raw_score, proficiency_bonus)


class Nature(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.INT, raw_score, proficiency_bonus)


class Religion(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.INT, raw_score, proficiency_bonus)


class AnimalHandling(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.WIS, raw_score, proficiency_bonus)


class Insight(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.WIS, raw_score, proficiency_bonus)


class Medicine(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.WIS, raw_score, proficiency_bonus)


class Perception(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.WIS, raw_score, proficiency_bonus)


class Survival(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.WIS, raw_score, proficiency_bonus)


class Deception(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.CHA, raw_score, proficiency_bonus)


class Intimidation(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.CHA, raw_score, proficiency_bonus)


class Performance(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.CHA, raw_score, proficiency_bonus)


class Persuasion(Skill):
    def __init__(self, raw_score: int, proficiency_bonus: int = 0) -> None:
        super().__init__(Ability.CHA, raw_score, proficiency_bonus)
