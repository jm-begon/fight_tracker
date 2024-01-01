from ..dice import Dice, Roll
from ..mechanics import Range, Skill, race
from ..mechanics.damage import DamageType
from ..mechanics.misc import Alignment
from ..mechanics.sense import Darkvision
from ..statblock import Action, PassiveAbility, StatBlock, StatBlockBuilder


class UndeadBuilder(StatBlockBuilder):
    def __init__(self, creature_name: str) -> None:
        super().__init__(creature_name)
        self.set_type("Undead")
        self.add_languages("Understand language it knew in life (cannot speak)")
        # TODO Poison immunity (damage & condition)


_zombie_builder = (
    UndeadBuilder("Zombie")
    .set_ability_scores(
        strength=13,
        dexterity=6,
        constitution=16,
        intelligence=3,
        wisdom=6,
        charisma=5,
    )
    .set_alignment(Alignment.NE)
    .set_level(3)
    .set_challenge_rating("1/4")
    .set_saving_throw_proficiencies(wisdom=True)
    # TODO Poison immunity (damage & condition)
    .add_senses(Darkvision(60))
    .add_languages("Understand language it knew in life (cannot speak)")
    .add_abilities(
        **{
            "Undead Fortitude": "If damage reduces this creature to 0 hit points, it must make a Constitution saving throw with a DC of 5 + the damage taken, unless the damage is radiant or from a critical hit. On a success, this creature drops to 1 hit point instead."
        }
    )
    .add_actions(
        Action.melee_weapon_attack(
            "Slam", 3, Roll.expected_outcome(6, +1), DamageType.BLUDGEONING
        )
    )
)


def create_zombie() -> StatBlock:
    return _zombie_builder.clone().create()


_zombie_grappler_builder = (
    _zombie_builder.clone()
    .override_name("Zombie Grappler")
    .set_ability_scores(strength=16)
    .add_skill_proficiencies(Skill.ATHLETICS)
    .add_abilities(Grappler="This creature has advantage of on grappling attacks.")
    .add_actions(
        Action(
            "Grab",
            (
                "+5 Strength (Athletics) check against an adjacent creature "
                "contested by a Strength (Athletics) / Dexterity (Acrobatics) "
                "check. In case of success, the target is grappled. The target "
                "creature can use its action to try to escape. When moving, "
                "the target is dragged but speed is halved."
            ),
            "Melee Attack",
        ),
        Action(
            "Bite",
            "Melee Weapon Attack: +3 to hit, reach 5 ft., one target. Hit: 3 (1d6) bludgeoning damage + 2 (1d4) poison damage."
            "Melee Attack",
        ),
    )
)


def create_zombie_grappler() -> StatBlock:
    return _zombie_grappler_builder.clone().create()


_zombie_Edric_Steadyhand_builder = (
    UndeadBuilder("Edric Steadyhand")
    .set_type("Undead (Dwarf)")
    .set_ability_scores(
        strength=13,
        dexterity=6,
        constitution=16,
        intelligence=3,
        wisdom=6,
        charisma=5,
    )
    .set_alignment(Alignment.NE)
    .set_armor_class(13, "Necrotic halo")
    .set_level(4)
    .set_challenge_rating("1/2")
    .set_saving_throw_proficiencies(wisdom=True)
    # TODO Poison immunity (damage & condition)
    .add_senses(Darkvision(60))
    .add_languages("Understand language it knew in life (cannot speak)")
    .add_abilities(
        **{
            "Necrotic release": (
                "When Edric Steadyhand dies, the Necrotic Echo which animates "
                "it jumps to the closest creature. The latter takes 12 (4d6) "
                "points of necrotic damage. If it is brought down to zero HP, "
                "it awakens a few minutes later with 1 HP, being the new host "
                " of the Necrotic Echo"
            )
        }
    )
    .add_actions(
        Action.melee_weapon_attack(
            "Spring Hammer",
            3,
            Roll.expected_outcome(8, +1),
            DamageType.BLUDGEONING,
            additional_info=(
                "On a successful hit, the spring activate, throwing "
                "the target 5 feet away on a failed DC 15 Strength (Athletics) "
                "(charges: 2)"
            ),
        ),
        Action(
            "Necrotic Influence",
            "When a nearby Zombie fails its `Undead Fortitude` save, it can try again once.",
            "Reaction",
        ),
    )
)


def create_edric_steadyhand() -> StatBlock:
    return _zombie_Edric_Steadyhand_builder.clone().create()


_skeleton_builder = (
    UndeadBuilder("Skeleton")
    .set_level(2)
    .set_alignment(Alignment.LE)
    .set_ability_scores(
        strength=10,
        dexterity=14,
        constitution=15,
        intelligence=6,
        wisdom=8,
        charisma=5,
    )
    .set_armor_class(13, "armor scraps")
    .set_speed(30)
    .add_senses(Darkvision(60))
    # TODO Damage vulnerabilities (Bludgeoning)
    .set_challenge_rating("1/4")
    .add_actions(
        Action.melee_weapon_attack(
            "Shortsword",
            4,
            Roll.expected_outcome(6, +2),
            DamageType.PIERCING,
        ),
        Action.ranged_weapon_attack(
            "Shortbow",
            4,
            Range(80, 320),
            Roll.expected_outcome(6, +2),
            DamageType.PIERCING,
        ),
    )
)


def create_skeleton() -> StatBlock:
    return _skeleton_builder.clone().create()
