from dataclasses import dataclass
from typing import Collection, Mapping

from .dice import Dice
from .mechanics.ability import Ability, AbilityScore, SavingThrow, Skill
from .mechanics.misc import Alignment, Size
from .mechanics.speed import Speed
from .rendering.card import Card, CardSeparator, Description
from .rendering.misc import HPBar
from .rendering.table import BoolCell, Table
from .typing import Intable


@dataclass
class Action:
    name: str
    description: str
    category: str | None = None


@dataclass
class StatBlock:
    name: str
    nickname: str | None = None
    proficency_bonus: int | None = None
    level: int | None = None
    size: Size | None = None
    category: str | None = None
    alignment: Alignment | None = None
    armor_class: Intable | None = None
    max_hit_points: Intable | None = None
    current_hit_points: int | None = None
    speed: Speed | None = None
    strength: Intable | None = None
    dexterity: Intable | None = None
    constitution: Intable | None = None
    intelligence: Intable | None = None
    wisdom: Intable | None = None
    charisma: Intable | None = None
    saving_throw_proficiencies: Collection[Ability] | None = None
    skill_proficiencies: Collection[Skill] | None = None
    passive_perception: int | None = None
    senses: Collection[
        str
    ] | None = None  # https://www.dndbeyond.com/sources/basic-rules/monsters#Senses
    languages: Collection[str] | None = None
    challenge_rating: str | None = None
    abilities: Mapping[str, str] | None = None
    actions: Collection[Action] | None = None

    @classmethod
    def compute_armor_class(
        cls, dice_sides: int, n_dices: int, cons_bonus: int
    ) -> Intable:
        return n_dices * Dice(dice_sides, rng="expectation") + n_dices * cons_bonus

    def __render__(self):
        if self.nickname is None:
            title = self.name
        else:
            title = f"{self.nickname} ({self.name})"

        card = Card(title)

        size_str = self.size.value.capitalize() if self.size else None
        info = " ".join([str(x) for x in [size_str, self.category] if x is not None])
        if len(info) < 2:
            info = None
        if self.alignment:
            alignment = self.alignment.value if self.alignment else None
            info = ", ".join([str(x) for x in [info, alignment] if x is not None])

        card.add(
            info,
            CardSeparator(),
            Description()
            .add_item("Armor Class", self.armor_class)
            .add_item(
                "Hit points", HPBar.create(self.max_hit_points, self.current_hit_points)
            )
            .add_item("Speed", self.speed),
        )

        ability_table = self._get_ability_table()

        card.add(
            ability_table,
            Description().add_item("Proficiency bonus", self.proficency_bonus)
            # TODO Damage resistances
            # TODO Damage immunities
            # TODO Condition immunities
            .add_item("Sense", list(self.senses) if self.senses is not None else None)
            .add_item(
                "Languages",
                ", ".join(str(lg) for lg in self.languages)
                if self.languages is not None
                else None,
            )
            .add_item("Challenge rating", self.challenge_rating),
            CardSeparator(),
        )
        ability_descr = Description()
        for name, descr in self.abilities.items():
            ability_descr.add_item(name, descr)

        action_descr = Description()
        for action in self.actions:
            descr = action.description
            if action.category:
                descr = f"{action.category}: {descr}"
            action_descr.add_item(action.name, descr)

        card.add(ability_descr, CardSeparator(), action_descr)

        # TODO legendary actions

        return card

    def _get_ability_table(self) -> Table:
        table = Table(header=True)
        table.fill_row(
            "",
            *[ability.name for ability in Ability],
        )
        table.fill_cell("Modifier")
        for ability in Ability:
            score = getattr(self, ability.value, None)
            if score is None:
                table.fill_cell("-")
            else:
                table.fill_cell(f"{AbilityScore.compute_modifier(score):+d}")

        table.delete_cell().new_row()

        table.fill_cell("Save")
        saving_throw_proficiencies = self.saving_throw_proficiencies or set()
        for ability in Ability:
            score = getattr(self, ability.value, None)
            if score is None:
                table.fill_cell("-")
                continue
            if self.proficency_bonus is None:
                table.fill_cell(BoolCell(ability in saving_throw_proficiencies))
            else:
                value = AbilityScore.compute_modifier(score)
                if ability in saving_throw_proficiencies:
                    value += int(self.proficency_bonus)

                table.fill_cell(f"{value:+d}")

        table.delete_cell()

        # TODO first row: ability modifiers
        # TODO second row: + prof bonus for saving throws

        return table
