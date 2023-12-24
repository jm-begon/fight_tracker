from __future__ import annotations

from abc import ABCMeta
from dataclasses import dataclass
from enum import Enum

from ..arithmetic import BaseIntable, DescriptiveInt
from ..typing import Intable


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
class AbilityScore(BaseIntable):
    ability: Ability
    score: Intable

    @property
    def modifier(self) -> int:
        return (int(self.score) - 10) // 2

    def __int__(self) -> int:
        return self.modifier

    def __str__(self) -> str:
        return f"{self.modifier} ({self.score} {self.ability.name})"

    @classmethod
    def strength(cls, raw_score: Intable) -> AbilityScore:
        return cls(Ability.STR, raw_score)

    @classmethod
    def dexterity(cls, raw_score: Intable) -> AbilityScore:
        return cls(Ability.DEX, raw_score)

    @classmethod
    def constitution(cls, raw_score: Intable) -> AbilityScore:
        return cls(Ability.CON, raw_score)

    @classmethod
    def intelligence(cls, raw_score: Intable) -> AbilityScore:
        return cls(Ability.INT, raw_score)

    @classmethod
    def wisdom(cls, raw_score: Intable) -> AbilityScore:
        return cls(Ability.WIS, raw_score)

    @classmethod
    def charisma(cls, raw_score: Intable) -> AbilityScore:
        return cls(Ability.CHA, raw_score)

    STR = strength
    DEX = dexterity
    CON = constitution
    INT = intelligence
    wIS = wisdom
    CHA = charisma


@dataclass
class SavingThrow(BaseIntable):
    ability_score: AbilityScore
    proficiency_bonus: Intable = 0

    def __int__(self) -> int:
        return int(self.ability_score) + int(self.proficiency_bonus)

    @classmethod
    def strength(
        cls, raw_score: Intable, proficiency_bonus: Intable = 0
    ) -> SavingThrow:
        return cls(AbilityScore.strength(raw_score), proficiency_bonus)

    @classmethod
    def dexterity(
        cls, raw_score: Intable, proficiency_bonus: Intable = 0
    ) -> SavingThrow:
        return cls(AbilityScore.dexterity(raw_score), proficiency_bonus)

    @classmethod
    def constitution(
        cls, raw_score: Intable, proficiency_bonus: Intable = 0
    ) -> SavingThrow:
        return cls(AbilityScore.constitution(raw_score), proficiency_bonus)

    @classmethod
    def intelligence(
        cls, raw_score: Intable, proficiency_bonus: Intable = 0
    ) -> SavingThrow:
        return cls(AbilityScore.intelligence(raw_score), proficiency_bonus)

    @classmethod
    def wisdom(cls, raw_score: Intable, proficiency_bonus: Intable = 0) -> SavingThrow:
        return cls(AbilityScore.wisdom(raw_score), proficiency_bonus)

    @classmethod
    def charisma(
        cls, raw_score: Intable, proficiency_bonus: Intable = 0
    ) -> SavingThrow:
        return cls(AbilityScore.charisma(raw_score), proficiency_bonus)

    STR = strength
    DEX = dexterity
    CON = constitution
    INT = intelligence
    wIS = wisdom
    CHA = charisma


class Skill(Enum):
    ATHLETICS = Ability.STR
    ACROBATICS = Ability.DEX
    SLEIGHT_OF_HAND = Ability.DEX
    ARCANA = Ability.INT
    HISTORY = Ability.INT
    INVESTIGATION = Ability.INT
    NATURE = Ability.INT
    RELIGION = Ability.INT
    ANIMAL_HANDLING = Ability.WIS
    MEDICINE = Ability.WIS
    PERCEPTION = Ability.WIS
    SURVIVAL = Ability.WIS
    DECEPTION = Ability.CHA
    INTIMIDATION = Ability.CHA
    PERFORMANCE = Ability.CHA
    PERSUASION = Ability.CHA


@dataclass
class SkillScore:
    ability_score: AbilityScore
    proficiency_bonus: Intable = 0

    def __int__(self) -> int:
        return int(self.ability_score) + int(self.proficiency_bonus)

    @classmethod
    def from_skill(
        cls, skill: Skill, raw_score: Intable, proficiency_bonus: Intable = 0
    ) -> SkillScore:
        return cls(AbilityScore(skill.value, raw_score), proficiency_bonus)
