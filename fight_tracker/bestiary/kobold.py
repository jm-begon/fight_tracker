from ..arithmetic import DescriptiveInt
from ..mechanics import Alignment, Darkvision, Size, Skill, speed
from ..statblock import Action, PassiveAbility, StatBlock, StatBlockBuilder


class KoboldBuilder(StatBlockBuilder):
    def __init__(self, creature_name: str) -> None:
        super().__init__(creature_name)
        self.set_size(Size.SMALL)
        self.set_type("Humanoid (Kobold)")
        self.set_alignment(Alignment.LE)
        self.set_speed(30)
        self.add_senses(Darkvision(60))
        self.add_languages("Common", "Draconic")
        self.add_abilities(
            PassiveAbility.pack_tactics(), PassiveAbility.sunlight_sensitivity()
        )
        self.add_actions(
            Action(
                "Dagger",
                "+4 to hit, range 30/120 ft., one target. Hit: 4 (1d4 + 2) bludgeoning damage.",
                "Ranged Weapon Attack",
            ),
            Action(
                "Sling",
                "+4 to hit, range 30/120 ft., one target. Hit: 4 (1d4 + 2) bludgeoning damage.",
                "Ranged Weapon Attack",
            ),
        )


_kobold_builder = (
    KoboldBuilder("Kobold")
    .set_ability_scores(
        strength=7,
        dexterity=15,
        constitution=9,
        intelligence=8,
        wisdom=7,
        charisma=8,
    )
    .set_level(2)
    .set_challenge_rating("1/8")
)


def create_kobold() -> StatBlock:
    return _kobold_builder.create()


_winged_builder = (
    KoboldBuilder("Winged Kobold")
    .set_ability_scores(
        strength=7,
        dexterity=16,
        constitution=9,
        intelligence=8,
        wisdom=7,
        charisma=8,
    )
    .set_level(2)
    .set_challenge_rating("1/4")
    .set_speed(speed.MultiSpeed(speed.Speed(30), speed.FlyingSpeed(30)))
    .add_action(
        "Drop Rock",
        "+5 to hit, one target directly below the kobold. Hit: 6 (1d6 + 3) bludgeoning damage.",
        "Ranged Weapon Attack",
    )
)


def create_winged_kobold() -> StatBlock:
    return _winged_builder.create()


_tracker_builder = (
    KoboldBuilder("Kobold Tracker")
    .set_ability_scores(
        strength=7,
        dexterity=15,
        constitution=9,
        intelligence=10,
        wisdom=16,
        charisma=8,
    )
    .set_level(3)
    .set_challenge_rating("1/2")
    .set_armor_class(DescriptiveInt(14, "natural armor"))
    .set_saving_throw_proficiencies(wisdom=True)
    .add_skill_proficiencies(Skill.SURVIVAL)
    .add_abilities(
        **{
            "Keen Smell": "The kobold tracker has advantage on Wisdom (Perception) checks that rely on smell.",
            "Infravision": "The kobold tracker can see in both magical and non-magical darkness as if it were bright light up to a distance of 60 feet.",
        },
    )
    .add_action(
        "Track",
        "1/Day. The kobold tracker can use its action to pinpoint the location of a specific creature it is familiar with, as long as the creature is within 1 mile and has left a scent trail within the last 24 hours.",
    )
)


def create_kobold_tracker() -> StatBlock:
    return _tracker_builder.create()
