from ..arithmetic import DescriptiveInt
from ..dice import Dice
from ..mechanics import Alignment, Size, Skill, speed
from ..mechanics.damage import DamageType
from ..statblock import Action, StatBlock, StatBlockBuilder

_thug_builder = (
    StatBlockBuilder("Thug")
    .set_ability_scores(
        strength=15,
        dexterity=11,
        constitution=14,
        intelligence=10,
        wisdom=10,
        charisma=11,
    )
    .set_proficiency_bonus(2)
    .set_level(5)
    .set_armor_class(11, "leather armor")
    .set_challenge_rating("1/2")
    .add_skill_proficiencies(Skill.INTIMIDATION)
    .add_abilities(
        **{
            "Pack Tactics": "The thug has advantage on an attack roll against a creature if at least one of the his allies is within 5 feet of the creature and the ally isn't incapacitated."
        }
    )
    .add_actions(
        Action.multiattack(2, "with his mace"),
        Action.melee_weapon_attack(
            "Mace", 4, Dice.expectation(6) + 2, DamageType.BLUDGEONING
        ),
        Action.ranged_weapon_attack(
            "Heavy Crossbow",
            2,
            "100/400 ft",
            Dice.expectation(10),
            DamageType.PIERCING,
        ),
    )
)


def create_thug_by_size(size: Size | None = None) -> StatBlock:
    if size is None:
        size = Size.MEDIUM
    # TODO by race instead
    builder = _thug_builder.clone()
    builder.set_size(size)
    return builder.create()
