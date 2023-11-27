from enum import Enum


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
