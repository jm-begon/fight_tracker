from ..dice import Dice, Roll
from ..mechanics import (
    Darkvision,
    FlyingSpeed,
    MultiSpeed,
    Range,
    Size,
    Skill,
    Speed,
    race,
)
from ..mechanics.damage import DamageType
from ..statblock import Action, PassiveAbility, StatBlock, StatBlockBuilder


class BeastBuilder(StatBlockBuilder):
    def __init__(self, creature_name: str) -> None:
        super().__init__(creature_name)
        self.set_type("Beast")


_stirge_builder = (
    BeastBuilder("Stirge")
    .set_ability_scores(
        strength=4,
        dexterity=16,
        constitution=11,
        intelligence=2,
        wisdom=8,
        charisma=6,
    )
    .set_level(1)
    .set_armor_class(14, "natural armor")
    .set_size(Size.TINY)
    .set_speed(MultiSpeed(Speed(10), FlyingSpeed(40)))
    .add_senses(Darkvision(60))
    .set_challenge_rating("1/8")
    .add_actions(
        Action(
            "Blood Drain",
            "+5 to hit, reach 5 ft., one creature. Hit: 5 (1d4 + 3) piercing damage, and the stirge attaches to the target. While attached, the stirge doesn't attack. Instead, at the start of each of the stirge's turns, the target loses 5 (1d4 + 3) hit points due to blood loss.",
            "Melee Weapon Attack",
        ),
        Action(
            "Detach",
            "The stirge can detach itself by spending 5 feet of its movement. It does so after it drains 10 hit points of blood from the target or the target dies. A creature, including the target, can use its action to detach the stirge.",
        ),
    )
)


def create_stirge() -> StatBlock:
    return _stirge_builder.create()
