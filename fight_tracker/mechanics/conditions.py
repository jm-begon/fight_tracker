from ..concept import Concept
from ..rendering.tree import Tree


class Condition(Concept):
    def short_repr(self):
        return self.__class__.__name__.lower()

    def long_repr(self):
        return Tree(self.short_repr())

    def can_move(self):
        return True

    def can_take_action(self):
        return True

    def __hash__(self):
        return hash(self.__class__.__name__)

    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__

    def __rshift__(self, creature):
        return creature.add_condition(self)


class Blinded(Condition):
    def long_repr(self):
        return (
            super()
            .long_repr()
            .add_children(
                "a blinded creature can’t see and automatically fails any ability "
                "check that requires sight",
                "attack rolls against the creature have advantage, and the "
                "creature’s Attack rolls have disadvantage",
            )
        )


class Charmed(Condition):
    def long_repr(self):
        return (
            super()
            .long_repr()
            .add_children(
                "a charmed creature can’t Attack the charmer or target the charmer "
                "with harmful Abilities or magical Effects",
                "the charmer has advantage on any ability check to interact "
                "socially with the creature",
            )
        )


class Deafened(Condition):
    def long_repr(self):
        return (
            super()
            .long_repr()
            .add_child(
                "a deafened creature can’t hear and automatically fails any ability check "
                "that requires hearing"
            )
        )


class Frightened(Condition):
    def long_repr(self):
        return (
            super()
            .long_repr()
            .add_children(
                "a frightened creature has disadvantage on Ability Checks and "
                "attack rolls while the source of its fear is within Line of Sight",
                "the creature can’t willingly move closer to the source of its fear",
            )
        )


class Incapacitated(Condition):
    def long_repr(self):
        return (
            super()
            .long_repr()
            .add_children("an incapacitated creature can’t take Actions or Reactions.")
        )

    def can_take_action(self):
        return False


class Grappled(Incapacitated):
    def long_repr(self):
        incap = Incapacitated.long_repr(self)
        incap.content = "incapacitated"
        return Condition.long_repr(self).add_children(
            incap,
            "a grappled creature’s speed becomes 0, and it can’t benefit from "
            "any bonus to its speed",
            "the condition also ends if an Effect removes the grappled creature "
            "from the reach of the Grappler or Grappling Effect, such as when a "
            "creature is hurled away",
        )


class Invisible(Condition):
    def long_repr(self):
        return (
            super()
            .long_repr()
            .add_children(
                "an invisible creature is impossible to see without the aid of "
                "magic or a Special sense. For the Purpose of Hiding, the creature "
                "is heavily obscured. The creature’s Location can be "
                "detected by any noise it makes or any tracks it leaves",
                "attack rolls against the creature have disadvantage, and the "
                "creature’s Attack rolls have advantage",
            )
        )


class Paralyzed(Incapacitated):
    def can_move(self):
        return False

    def long_repr(self):
        incap = Incapacitated.long_repr(self)
        incap.content = "incapacitated"
        return Condition.long_repr(self).add_children(
            incap,
            "a paralyzed creature can speak of move",
            "the creature automatically fails Strength and Dexterity Saving " "Throws",
            "attack rolls against the creature have advantage",
            "any Attack that hits the creature is a critical hit if the "
            "attacker is within 5 feet of the creature",
        )


class Petrified(Incapacitated):
    def can_move(self):
        return False

    def long_repr(self):
        incap = Incapacitated.long_repr(self)
        incap.content = "incapacitated"
        return Condition.long_repr(self).add_children(
            incap,
            "a petrified creature can’t move or speak, and is unaware of its "
            "surroundings",
            "the creature s transformed, along with any nonmagical object it "
            "is wearing or carrying, into a solid inanimate substance "
            "(usually stone). Its weight increases by a factor of ten, and "
            "it ceases aging",
            "attack rolls against the creature have advantage",
            "the creature automatically fails Strength and Dexterity Saving " "Throws",
            "the creature has Resistance to all damage",
            "the creature is immune to poison and disease, although a poison "
            "or disease already in its system is suspended, not neutralized",
        )


class Poisoned(Condition):
    def long_repr(self):
        return (
            super()
            .long_repr()
            .add_children(
                "a poisoned creature has disadvantage on Attack rolls and "
                "Ability Checks"
            )
        )


class Prone(Condition):
    def long_repr(self):
        return (
            super()
            .long_repr()
            .add_children(
                "a prone creature’s only Movement option is to crawl, unless it "
                "stands up and thereby ends the condition",
                "the creature has disadvantage on Attack rolls",
                "an Attack roll against the creature has advantage if the attacker "
                "is within 5 feet of the creature. Otherwise, the Attack "
                "roll has disadvantage",
            )
        )


class Restrained(Condition):
    def can_move(self):
        return False

    def long_repr(self):
        return (
            super()
            .long_repr()
            .add_children(
                "A restrained creature’s speed becomes 0, and it can’t benefit from any bonus to its speed.",
                "Attack rolls against the creature have advantage, and the creature’s Attack rolls have disadvantage.",
                "The creature has disadvantage on Dexterity Saving Throws",
            )
        )


class Stunned(Incapacitated):
    def can_move(self):
        return False

    def long_repr(self):
        incap = Incapacitated.long_repr(self)
        incap.content = "incapacitated"
        return Condition.long_repr(self).add_children(
            incap,
            "a stunned creature can’t move, and can speak only falteringly"
            "the creature automatically fails Strength and Dexterity Saving "
            "Throws",
            "attack rolls against the creature have advantage",
        )


class Unconscious(Incapacitated, Prone):
    def can_move(self):
        return False

    def can_take_action(self):
        return False

    def long_repr(self):
        root = Condition.long_repr(self)
        incap = Incapacitated.long_repr(self)
        incap.content = "incapacitated"
        prone = Prone.long_repr(self)
        prone.content = "prone"
        return root.add_children(
            incap,
            "an unconscious creature can’t move or speak, and is unaware of "
            "its surroundings",
            "the creature drops whatever it’s holding and falls prone",
            prone,
            "the creature automatically fails Strength and Dexterity Saving " "Throws",
            "attack rolls against the creature have advantage",
            "any Attack that hits the creature is a critical hit if the "
            "attacker is within 5 feet of the creature",
        )


class Dead(Unconscious):
    def long_repr(self):
        return (
            super().long_repr().add_children("a dead creature cannot be played anymore")
        )


class Exhausted(Condition):
    def __init__(self, level=1):
        self.level = level

    def __iadd__(self, other):
        self.level += other

    def __isub__(self, other):
        self.level -= other

    def can_take_action(self):
        return self.level < 6

    def can_move(self):
        return self.level < 5

    def long_repr(self):
        eff_list = [
            "1: disadvantage on Ability Checks",
            "2: speed halved",
            "3: disadvantage on Attack rolls and Saving Throws",
            "4: hit point maximum halved",
            "5: speed reduced to 0",
            "6: death",
        ]

        for i in range(len(eff_list)):
            prefix = ">" if self.level == (i + 1) else " "
            eff_list[i] = prefix + eff_list[i]

        effect = Tree("Effects by level").add_children(*eff_list)
        return (
            super()
            .long_repr()
            .add_children(
                "if an already exhausted creature suffers another Effect that"
                " causes exhaustion, its current level of exhaustion increases by"
                " the amount specified in the effect’s description",
                "a creature suffers the Effect of its current level of exhaustion"
                " as well as all lower levels. For example, a creature suffering"
                " level 2 exhaustion has its speed halved and has disadvantage on"
                " Ability Checks",
                "an Effect that removes exhaustion reduces its level as specified"
                " in the effect’s description, with all exhaustion Effects Ending"
                " if a creature’s exhaustion level is reduced below 1",
                "finishing a Long Rest reduces a creature’s exhaustion level by 1,"
                " provided that the creature has also ingested some food and drink",
                effect,
            )
        )

    def __hash__(self):
        return super(Exhausted, self).__hash__() + hash(self.level)

    def __eq__(self, other):
        return super(Exhausted, self).__eq__(other) and self.level == other.level
