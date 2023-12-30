from ..arithmetic import DescriptiveInt
from ..dice import Dice, Roll
from ..mechanics import Range, Skill, race
from ..mechanics.damage import DamageType
from ..statblock import Action, PassiveAbility, StatBlock, StatBlockBuilder


def apply_race(builder: StatBlockBuilder, creature_race: race.Race | None = None):
    if creature_race is None:
        creature_race = race.HUMAN

    builder.apply_racial_traits(creature_race)


_bandit_builder = (
    StatBlockBuilder("Bandit")
    .set_ability_scores(
        strength=11,
        dexterity=12,
        constitution=12,
        intelligence=10,
        wisdom=10,
        charisma=10,
    )
    .set_level(2)
    .set_armor_class(12, "leather armor")
    .set_challenge_rating("1/8")
    .add_actions(
        Action.melee_weapon_attack(
            "Scimitar", 3, Roll.outcome(Dice.expectation(6) + 1), DamageType.SLASHING
        ),
        Action.ranged_weapon_attack(
            "Light Crossbow",
            3,
            Range(80, 320),
            Roll.outcome(Dice.expectation(8) + 1),
            DamageType.PIERCING,
        ),
    )
)


def create_bandit(creature_race: race.Race | None = None) -> StatBlock:
    builder = _bandit_builder.clone()
    apply_race(builder, creature_race)

    return builder.create()


_wizard_apprentice_builder = (
    StatBlockBuilder("Wizard apprentice")
    .set_ability_scores(
        strength=10,
        dexterity=10,
        constitution=10,
        intelligence=14,
        wisdom=10,
        charisma=12,
    )
    .set_level(3)
    .set_armor_class(10)
    .set_challenge_rating("1/4")
    .add_skill_proficiencies(Skill.ARCANA, Skill.HISTORY)
    .add_actions(
        Action.melee_spell_attack(
            "Arcane burst",
            4,
            Roll.outcome(Dice.expectation(10) + 2),
            DamageType.FORCE,
        ),
        Action.ranged_spell_attack(
            "Firebolt",
            4,
            Range(120),
            Roll.outcome(Dice.expectation(10) + 2),
            DamageType.FIRE,
        ),
        Action("Shield", "1/day, +5 AC as reaction (until start of next turn)"),
        Action(
            "Spill balls",
            "1 charge, cover an adjacent 10-feet square ground with metal balls. The terrain becomes difficult (or must succeed a DC 12 DEX save).",
        ),
    )
)


def create_apprentice_wizard(creature_race: race.Race | None = None) -> StatBlock:
    builder = _wizard_apprentice_builder.clone()
    apply_race(builder, creature_race)

    return builder.create()


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
            Range(100, 400),
            Roll.outcome(Dice.expectation(10)),
            DamageType.PIERCING,
        ),
    )
)


def create_thug(creature_race: race.Race | None = None) -> StatBlock:
    builder = _thug_builder.clone()
    apply_race(builder, creature_race)

    return builder.create()
