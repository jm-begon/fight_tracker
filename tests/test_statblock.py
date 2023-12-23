from fight_tracker.arithmetic import DescriptiveInt
from fight_tracker.dice import Dice
from fight_tracker.mechanics.misc import Alignment, Size
from fight_tracker.mechanics.speed import Speed
from fight_tracker.rendering import StreamRenderer
from fight_tracker.statblock import Action, StatBlock


def test_stream_render() -> None:
    sr = StreamRenderer()

    kobold = StatBlock(
        name="Kobold Tracker",
        nickname="Kb1",
        proficency_bonus=2,
        level=4,
        size=Size.SMALL,
        category="humanoid (kobold)",
        alignment=Alignment.LE,
        armor_class=DescriptiveInt(13, "natural armor"),
        max_hit_points=3 * Dice(6, "expectation") + 3,
        speed=Speed(30),
        ability_modifiers=set(),
        skills=set(),
        passive_perception=12,
        senses=("Darkvision 60ft"),
        languages=("Common", "Draconic"),
        challenge_rating="1/2",
        abilities={
            "Sunlight Sensitivity": "While in sunlight, the kobold tracker has disadvantage on attack rolls, as well as on Wisdom (Perception) checks that rely on sight.",
            "Pack Tactics": "The kobold tracker has advantage on an attack roll against a creature if at least one of the kobold's allies is within 5 feet of the creature and the ally isn't incapacitated.",
            "Keen Smell": "The kobold tracker has advantage on Wisdom (Perception) checks that rely on smell.",
            "Infravision": "The kobold tracker can see in both magical and non-magical darkness as if it were bright light up to a distance of 60 feet.",
        },
        actions=(
            Action(
                "Shortsword",
                "+4 to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) piercing damage."
                "Melee Weapon Attack",
            ),
            Action(
                "Sling",
                "+4 to hit, range 30/120 ft., one target. Hit: 4 (1d4 + 2) bludgeoning damage.",
                "Ranged Weapon Attack",
            ),
            Action(
                "Track",
                "Special",
                "1/Day. The kobold tracker can use its action to pinpoint the location of a specific creature it is familiar with, as long as the creature is within 1 mile and has left a scent trail within the last 24 hours.",
            ),
        ),
    )

    sr << kobold
    # assert False
