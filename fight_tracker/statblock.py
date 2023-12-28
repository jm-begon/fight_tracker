from dataclasses import dataclass
from typing import Collection, Dict, Mapping, cast

from .dice import Dice
from .mechanics.ability import Ability, AbilityScore, SavingThrow, Skill
from .mechanics.misc import Alignment, Size
from .mechanics.speed import Speed
from .rendering.card import Card, CardSeparator, Description
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
    proficency_bonus: int | None = None
    size: Size | None = None
    category: str | None = None
    alignment: Alignment | None = None
    armor_class: Intable | None = None
    max_hit_points: Intable | None = None
    speed: Speed | None = None
    strength: Intable | None = None
    dexterity: Intable | None = None
    constitution: Intable | None = None
    intelligence: Intable | None = None
    wisdom: Intable | None = None
    charisma: Intable | None = None
    saving_throw_proficiencies: Collection[Ability] | None = None
    skill_proficiencies: Collection[Skill] | None = None
    initiative_bonus: int | None = None
    passive_perception: int | None = None
    # TODO # https://www.dndbeyond.com/sources/basic-rules/monsters#Senses
    senses: Collection[str] | None = None
    languages: Collection[str] | None = None
    challenge_rating: str | None = None
    abilities: Mapping[str, str] | None = None
    actions: Collection[Action] | None = None
    # immunities:  # condition or dmg types
    # resistances: # condition or dmg types

    def __post_init__(self):
        if self.initiative_bonus is None and self.dexterity is not None:
            self.initiative_bonus = AbilityScore.dexterity(self.dexterity).modifier

        if self.proficency_bonus is None:
            self.proficency_bonus = 0

        self.saving_throw_proficiencies = self.saving_throw_proficiencies or set()
        self.skill_proficiencies = self.skill_proficiencies or set()

    @property
    def strength_score(self) -> AbilityScore | None:
        return AbilityScore.strength(self.strength) if self.strength else None

    @property
    def strength_saving_throw(self) -> SavingThrow | None:
        pb = cast(
            int,
            self.proficency_bonus
            if self.saving_throw_proficiencies
            and Ability.STR in self.saving_throw_proficiencies
            else 0,
        )
        return SavingThrow.strength(self.strength, pb) if self.strength else None

    @property
    def dexterity_score(self) -> AbilityScore | None:
        return AbilityScore.dexterity(self.dexterity) if self.dexterity else None

    @property
    def dexterity_saving_throw(self) -> SavingThrow | None:
        pb = cast(
            int,
            self.proficency_bonus
            if self.saving_throw_proficiencies
            and Ability.DEX in self.saving_throw_proficiencies
            else 0,
        )
        return SavingThrow.dexterity(self.dexterity, pb) if self.dexterity else None

    @property
    def constitution_score(self) -> AbilityScore | None:
        return (
            AbilityScore.constitution(self.constitution) if self.constitution else None
        )

    @property
    def constitution_saving_throw(self) -> SavingThrow | None:
        pb = cast(
            int,
            self.proficency_bonus
            if self.saving_throw_proficiencies
            and Ability.CON in self.saving_throw_proficiencies
            else 0,
        )
        return (
            SavingThrow.constitution(self.constitution, pb)
            if self.constitution
            else None
        )

    @property
    def intelligence_score(self) -> AbilityScore | None:
        return (
            AbilityScore.intelligence(self.intelligence) if self.intelligence else None
        )

    @property
    def intelligence_saving_throw(self) -> SavingThrow | None:
        pb = cast(
            int,
            self.proficency_bonus
            if self.saving_throw_proficiencies
            and Ability.INT in self.saving_throw_proficiencies
            else 0,
        )
        return (
            SavingThrow.intelligence(self.intelligence, pb)
            if self.intelligence
            else None
        )

    @property
    def wisdom_score(self) -> AbilityScore | None:
        return AbilityScore.wisdom(self.wisdom) if self.wisdom else None

    @property
    def wisdom_saving_throw(self) -> SavingThrow | None:
        pb = cast(
            int,
            self.proficency_bonus
            if self.saving_throw_proficiencies
            and Ability.WIS in self.saving_throw_proficiencies
            else 0,
        )
        return SavingThrow.wisdom(self.wisdom, pb) if self.wisdom else None

    @property
    def charisma_score(self) -> AbilityScore | None:
        return AbilityScore.charisma(self.charisma) if self.charisma else None

    @property
    def charisma_saving_throw(self) -> SavingThrow | None:
        pb = cast(
            int,
            self.proficency_bonus
            if self.saving_throw_proficiencies
            and Ability.CHA in self.saving_throw_proficiencies
            else 0,
        )
        return SavingThrow.charisma(self.charisma, pb) if self.charisma else None

    def get_saving_throw(self, ability: Ability) -> SavingThrow | None:
        return getattr(self, f"{ability.value}_saving_throw")

    def get_ability_score(self, ability: Ability) -> AbilityScore | None:
        return getattr(self, f"{ability.value}_score")

    def get_ability_scores(self) -> Dict[Ability, AbilityScore]:
        ans = {ability: self.get_ability_score(ability) for ability in Ability}
        return {k: v for k, v in ans.items() if v is not None}

    def get_saving_throws(self) -> Dict[Ability, SavingThrow]:
        ans = {ability: self.get_saving_throw(ability) for ability in Ability}
        return {k: v for k, v in ans.items() if v is not None}

    def __render__(self):
        card = Card(self.name)

        size_str = self.size.value.capitalize() if self.size else None
        info = " ".join([str(x) for x in [size_str, self.category] if x is not None])
        if len(info) < 2:
            info = None
        if self.alignment:
            alignment = self.alignment.value if self.alignment else None
            info = ", ".join([str(x) for x in [info, alignment] if x is not None])

        hp_str = None
        if self.max_hit_points:
            hp_str = str(self.max_hit_points)
            hp_int = int(self.max_hit_points)
            if hp_str != str(hp_int):
                hp_str = f"{hp_int} ({hp_str})"
        card.add(
            info,
            CardSeparator(),
            Description()
            .add_item("Armor Class", self.armor_class)
            .add_item("Hit points", hp_str)
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
        )
        if self.abilities:
            ability_descr = Description()
            for name, descr in self.abilities.items():
                ability_descr.add_item(name, descr)
            card.add(CardSeparator(), ability_descr)

        if self.actions:
            action_descr = Description()
            for action in self.actions:
                descr = action.description
                if action.category:
                    descr = f"{action.category}: {descr}"
                action_descr.add_item(action.name, descr)

            card.add(CardSeparator("Action"), action_descr)

        # TODO legendary actions

        return card

    def fill_ability_modifier_table(
        self, table: Table, label: str | None = None
    ) -> Table:
        if label:
            table.fill_cell(label)
        scores = self.get_ability_scores()
        for ability in Ability:
            if ability in scores:
                table.fill_cell(f"{int(scores[ability]):+d}")
            else:
                table.fill_cell("-")

        table.delete_cell()
        return table

    def fill_saving_throw_table(self, table: Table, label: str | None = None) -> Table:
        if label:
            table.fill_cell(label)
        saving_throw_proficiencies = self.saving_throw_proficiencies or set()
        throws = self.get_saving_throws()
        for ability in Ability:
            if ability in throws:
                table.fill_cell(f"{int(throws[ability]):+d}")
            elif (
                self.proficency_bonus is not None
                and len(saving_throw_proficiencies) > 0
            ):
                table.fill_cell(BoolCell(ability in saving_throw_proficiencies))
            else:
                table.fill_cell("-")

        table.delete_cell()
        return table

    def _get_ability_table(self) -> Table:
        table = Table(header=True)
        table.fill_row(
            "",
            *[ability.name for ability in Ability],
        )
        self.fill_ability_modifier_table(table, "Modifier").new_row()
        self.fill_saving_throw_table(table, "Save")

        return table
