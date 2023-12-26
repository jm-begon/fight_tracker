import os
from io import StringIO

from fight_tracker.arithmetic import DescriptiveInt
from fight_tracker.dice import Dice, Roll
from fight_tracker.mechanics.ability import Ability
from fight_tracker.mechanics.misc import Alignment, Size
from fight_tracker.mechanics.speed import Speed
from fight_tracker.rendering import StreamRenderer
from fight_tracker.statblock import Action, StatBlock


def test_stream_render() -> None:
    buffer = StringIO()
    sr = StreamRenderer(buffer)

    kobold = StatBlock(
        name="Kobold Tracker",
        nickname="Kb1",
        proficency_bonus=2,
        level=3,
        size=Size.SMALL,
        category="humanoid (kobold)",
        alignment=Alignment.LE,
        armor_class=DescriptiveInt(13, "natural armor"),
        max_hit_points=3 * Dice(6, "expectation") + 3,
        speed=Speed(30),
        strength=7,
        dexterity=15,
        constitution=9,
        intelligence=8,
        wisdom=7,
        charisma=8,
        saving_throw_proficiencies=(Ability.WIS,),
        skill_proficiencies=None,  # TODO
        passive_perception=12,
        senses=("Darkvision 60ft",),
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
                "+4 to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) piercing damage.",
                "Melee Weapon Attack",
            ),
            Action(
                "Sling",
                "+4 to hit, range 30/120 ft., one target. Hit: 4 (1d4 + 2) bludgeoning damage.",
                "Ranged Weapon Attack",
            ),
            Action(
                "Track",
                "1/Day. The kobold tracker can use its action to pinpoint the location of a specific creature it is familiar with, as long as the creature is within 1 mile and has left a scent trail within the last 24 hours.",
            ),
        ),
    )

    sr(kobold)
    given = sr.strip_formating(buffer.getvalue()).split(os.linesep)

    expected = """/------------------------------------------------------------------------------+
| KB1 (KOBOLD TRACKER)                                                         |
| Small humanoid (kobold), lawful evil                                         |
| ---------------------------------------------------------------------------- |
| - Armor Class: 13 (natural armor)                                            |
| - Hit points: 12 (3d6 + 3)                                                   |
| - Speed: 6.0 sq                                                              |
| /----------+-----+-----+-----+-----+-----+-----+                             |
| |          | STR | DEX | CON | INT | WIS | CHA |                             |
| +----------+-----+-----+-----+-----+-----+-----+                             |
| | Modifier | -2  | +2  | -1  | -1  | -2  | -1  |                             |
| | Save     | -2  | +2  | -1  | -1  | +0  | -1  |                             |
| +----------+-----+-----+-----+-----+-----+-----/                             |
| - Proficiency bonus: 2                                                       |
| - Sense: Darkvision 60ft                                                     |
| - Languages: Common, Draconic                                                |
| - Challenge rating: 1/2                                                      |
| ---------------------------------------------------------------------------- |
| - Sunlight Sensitivity: While in sunlight, the kobold tracker has            |
| disadvantage on attack rolls, as well as on Wisdom (Perception) checks that  |
| rely on sight.                                                               |
| - Pack Tactics: The kobold tracker has advantage on an attack roll           |
| against a creature if at least one of the kobold's allies is within 5 feet   |
| of the creature and the ally isn't incapacitated.                            |
| - Keen Smell: The kobold tracker has advantage on Wisdom                     |
| (Perception) checks that rely on smell.                                      |
| - Infravision: The kobold tracker can see in both magical and                |
| non-magical darkness as if it were bright light up to a distance of 60 feet. |
| ----------------------------------------------------------------------Action |
| - Shortsword: Melee Weapon Attack: +4 to hit, reach 5 ft., one               |
| target. Hit: 5 (1d6 + 2) piercing damage.                                    |
| - Sling: Ranged Weapon Attack: +4 to hit, range 30/120 ft., one              |
| target. Hit: 4 (1d4 + 2) bludgeoning damage.                                 |
| - Track: 1/Day. The kobold tracker can use its action to pinpoint            |
| the location of a specific creature it is familiar with, as long as the      |
| creature is within 1 mile and has left a scent trail within the last 24      |
| hours.                                                                       |
+------------------------------------------------------------------------------/""".split(
        os.linesep
    )
    for i in range(len(expected)):
        assert given[i] == expected[i]


def test_stream_render_small() -> None:
    buffer = StringIO()
    sr = StreamRenderer(buffer)

    kobold = StatBlock(
        name="Kobold Tracker",
        armor_class=13,
        max_hit_points=12,
    )

    sr(kobold)
    print(sr.strip_formating(buffer.getvalue()))
    assert False
