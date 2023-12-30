from ..arithmetic import DescriptiveInt
from ..dice import Dice, Roll
from ..mechanics import Skill, race
from ..mechanics.damage import DamageType
from ..statblock import Action, PassiveAbility, StatBlock, StatBlockBuilder


def apply_race(builder: StatBlockBuilder, creature_race: race.Race | None = None):
    if creature_race is None:
        creature_race = race.HUMAN

    builder.apply_racial_traits(creature_race)


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
        PassiveAbility.pack_tactics(),
    )
    .add_actions(
        Action.multiattack(2, "with his mace"),
        Action.melee_weapon_attack(
            "Mace", 4, Roll.outcome(Dice.expectation(6) + 2), DamageType.BLUDGEONING
        ),
        Action.ranged_weapon_attack(
            "Heavy Crossbow",
            2,
            "100/400 ft",
            Roll.outcome(Dice.expectation(10)),
            DamageType.PIERCING,
        ),
    )
)


def create_thug(creature_race: race.Race | None = None) -> StatBlock:
    builder = _thug_builder.clone()
    apply_race(builder, creature_race)

    return builder.create()
