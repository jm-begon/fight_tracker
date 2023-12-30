from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Collection, Dict, List, Self, Sequence, cast

from .arithmetic import DescriptiveInt
from .dice import Dice, Roll
from .mechanics.ability import Ability, AbilityScore, SavingThrow, Skill
from .mechanics.damage import DamageType
from .mechanics.misc import Alignment, Size
from .mechanics.race import Race
from .mechanics.sense import Sense
from .mechanics.speed import Distance, Range, Speed, Unit
from .rendering.card import Card, CardSeparator, Description
from .rendering.table import BoolCell, Table
from .typing import Intable


@dataclass
class Action:
    name: str
    description: str | Any  # Any renderable
    category: str | None = None

    @classmethod
    def multiattack(cls, how_many: int, which_attack: str | None = None) -> Action:
        desc = f"This creature makes {how_many} attacks."
        if which_attack:
            desc = f"{desc[:-1]}; {which_attack}."

        return cls("Multiattack", desc)

    @classmethod
    def melee_attack(
        cls,
        category: str,
        name: str,
        hit_bonus: int,
        damage: Intable,
        damage_type: DamageType | None = None,
        how_many_targets: int | None = None,
        reach: Distance | None = None,
    ) -> Action:
        damage_type_str = f" {damage_type.value}" if damage_type else ""
        if reach is None:
            reach = Distance(5)
        how_many_targets = 1 if how_many_targets is None else how_many_targets
        desc = [
            f"{hit_bonus:+d} to hit, reach",
            reach,
            f", {how_many_targets} target(s). Hit {damage}{damage_type_str} damage.",
        ]
        return cls(name, desc, category)

    @classmethod
    def melee_weapon_attack(
        cls,
        name: str,
        hit_bonus: int,
        damage: Intable,
        damage_type: DamageType | None = None,
        how_many_targets: int | None = None,
        reach: Distance | None = None,
    ) -> Action:
        return cls.melee_attack(
            "Melee Weapon Attack",
            name=name,
            hit_bonus=hit_bonus,
            damage=damage,
            damage_type=damage_type,
            how_many_targets=how_many_targets,
            reach=reach,
        )

    @classmethod
    def melee_spell_attack(
        cls,
        name: str,
        hit_bonus: int,
        damage: Intable,
        damage_type: DamageType | None = None,
        how_many_targets: int | None = None,
        reach: Distance | None = None,
    ) -> Action:
        return cls.melee_attack(
            "Melee Spell Attack",
            name=name,
            hit_bonus=hit_bonus,
            damage=damage,
            damage_type=damage_type,
            how_many_targets=how_many_targets,
            reach=reach,
        )

    @classmethod
    def range_attack(
        cls,
        category: str,
        name: str,
        hit_bonus: int,
        range: Range,
        damage: Intable,
        damage_type: DamageType | None = None,
        how_many_targets: int | None = None,
    ) -> Action:
        damage_type_str = f" {damage_type.value}" if damage_type else ""
        how_many_targets = 1 if how_many_targets is None else how_many_targets
        desc = [
            f"{hit_bonus:+d} to hit, range",
            range,
            f", {how_many_targets} target(s). Hit {damage}{damage_type_str} damage.",
        ]
        return cls(name, desc, category)

    @classmethod
    def ranged_weapon_attack(
        cls,
        name: str,
        hit_bonus: int,
        range: Range,
        damage: Intable,
        damage_type: DamageType | None = None,
        how_many_targets: int | None = None,
    ) -> Action:
        return cls.range_attack(
            "Range Weapon Attack",
            name=name,
            hit_bonus=hit_bonus,
            range=range,
            damage=damage,
            damage_type=damage_type,
            how_many_targets=how_many_targets,
        )

    @classmethod
    def ranged_spell_attack(
        cls,
        name: str,
        hit_bonus: int,
        range: Range,
        damage: Intable,
        damage_type: DamageType | None = None,
        how_many_targets: int | None = None,
    ) -> Action:
        return cls.range_attack(
            "Range Spell Attack",
            name=name,
            hit_bonus=hit_bonus,
            range=range,
            damage=damage,
            damage_type=damage_type,
            how_many_targets=how_many_targets,
        )


@dataclass
class PassiveAbility:
    name: str
    effect: str

    @classmethod
    def pack_tactics(cls) -> PassiveAbility:
        return cls(
            "Pack Tactics",
            "This creature has advantage on an attack roll against an opponent if at least one of the his allies is within 5 feet of the opponent and the ally isn't incapacitated.",
        )

    @classmethod
    def sunlight_sensitivity(cls) -> PassiveAbility:
        return cls(
            "Sunlight Sensitivity",
            "While in sunlight, this creature has disadvantage on attack rolls, as well as on Wisdom (Perception) checks that rely on sight.",
        )

    @classmethod
    def keen_smell(cls) -> PassiveAbility:
        return cls(
            "Keen Smell",
            "This creature has advantage on Wisdom (Perception) checks that rely on smell.",
        )


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
    senses: Collection[Sense] | None = None
    languages: Collection[str] | None = None
    challenge_rating: str | None = None
    abilities: Collection[PassiveAbility] | None = None
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

        if self.senses:
            sense_list = list(self.senses)
        else:
            sense_list = []
        if self.passive_perception:
            sense_list.append(f"Passive perception {self.passive_perception}")
        if len(sense_list) > 0:
            sense_list = self.add_separator(sense_list)
        else:
            sense_list = None  # remove line

        card.add(
            ability_table,
            Description().add_item("Proficiency bonus", self.proficency_bonus)
            # TODO Damage resistances
            # TODO Damage immunities
            # TODO Condition immunities
            .add_item("Senses", sense_list)
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
            for ability in self.abilities:
                ability_descr.add_item(ability.name, ability.effect)
            card.add(CardSeparator(), ability_descr)

        if self.actions:
            action_descr = Description()
            for action in self.actions:
                descr = []
                if action.category:
                    descr.append(f"{action.category}:")
                descr.append(action.description)
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

    def add_separator(self, ls: Sequence, sep: str = "/") -> List:
        if len(ls) < 2:
            return list(ls)
        res: List[Any] = [None] * (2 * len(ls) - 1)
        res[::2] = ls
        res[1::2] = [sep] * (len(ls) - 1)
        return res


@dataclass
class InferredInt:
    value: int

    def __int__(self) -> int:
        return self.value


class StatBlockBuilder:
    def __init__(self, creature_name: str) -> None:
        self.stat_block = StatBlock(
            name=creature_name,
            size=Size.MEDIUM,
        )
        self.level: int | None = None
        self._hit_dice: Dice | None = None

    def set_proficiency_bonus(self, proficiency_bonus: int | None) -> Self:
        if proficiency_bonus:
            self.stat_block.proficency_bonus = proficiency_bonus
        return self

    def infer_proficiency_bonus(self) -> None:
        pb = self.stat_block.proficency_bonus
        if pb is not None and pb != 0:
            return
        if self.level:
            self.set_proficiency_bonus(2 + ((int(self.level) - 1) // 4))

    def set_hit_dice(self, value: int | None) -> Self:
        if value:
            self._hit_dice = Dice(value, "expectation")
        return self

    @property
    def hit_dice(self) -> Dice | None:
        if self._hit_dice:
            return self._hit_dice

        v: int | None = None
        size = self.stat_block.size
        if size == Size.TINY:
            v = 4
        elif size == Size.SMALL:
            v = 6
        elif size == Size.MEDIUM:
            v = 8
        elif size == Size.LARGE:
            v = 10
        elif size == Size.HUGE:
            v = 12
        elif size == Size.GARGANTUAN:
            v = 20

        if v is None:
            return None

        return Dice(v, "expectation")

    def set_type(self, category: str | None) -> Self:
        if category:
            self.stat_block.category = category
        return self

    set_category = set_type

    def set_alignment(self, alignment: Alignment | None) -> Self:
        if alignment:
            self.stat_block.alignment = alignment
        return self

    def set_armor_class(
        self,
        armor_class: Intable | None,
        description: str | None = None,
    ) -> Self:
        if armor_class:
            if description is not None:
                armor_class = DescriptiveInt(armor_class, description)
            self.stat_block.armor_class = armor_class
        return self

    def infer_armor_class(self) -> None:
        if self.stat_block.armor_class:
            return

        dexterity_score = self.stat_block.dexterity_score
        if dexterity_score:
            self.stat_block.armor_class = 10 + dexterity_score.modifier

    def set_max_hit_points(self, max_hit_points: Intable | None) -> Self:
        if max_hit_points:
            self.stat_block.max_hit_points = max_hit_points
        return self

    def infer_max_hit_points(self) -> None:
        hp = self.stat_block.max_hit_points
        if hp is not None:
            return

        if (
            not self.level
            or not self.stat_block.constitution_score
            or not self.hit_dice
        ):
            return

        self.set_max_hit_points(
            self.level * self.hit_dice
            + (self.level * self.stat_block.constitution_score.modifier)
        )

    def set_init_bonus(self, initiative_bonus: int | None) -> Self:
        if initiative_bonus:
            self.stat_block.initiative_bonus = initiative_bonus
        return self

    def infer_init_bonus(self) -> None:
        if self.stat_block.initiative_bonus:
            return
        dexterity_score = self.stat_block.dexterity_score
        if dexterity_score:
            self.set_init_bonus(dexterity_score.modifier)

    def set_passive_perception(self, passive_perception: int | None) -> Self:
        if passive_perception:
            self.stat_block.passive_perception = passive_perception
        return self

    def infer_passive_perception(self) -> None:
        if self.stat_block.wisdom_score is None:
            return

        score = 10 + self.stat_block.wisdom_score.modifier

        if (
            self.stat_block.skill_proficiencies
            and Skill.PERCEPTION in self.stat_block.skill_proficiencies
        ):
            pb = self.stat_block.proficency_bonus
            score = score + (pb if pb is not None else 0)

        self.stat_block.passive_perception = score

    def set_ability_scores(
        self,
        strength: Intable | None = None,
        dexterity: Intable | None = None,
        constitution: Intable | None = None,
        intelligence: Intable | None = None,
        wisdom: Intable | None = None,
        charisma: Intable | None = None,
    ) -> Self:
        if strength:
            self.stat_block.strength = strength
        if dexterity:
            self.stat_block.dexterity = dexterity
        if constitution:
            self.stat_block.constitution = constitution
        if intelligence:
            self.stat_block.intelligence = intelligence
        if wisdom:
            self.stat_block.wisdom = wisdom
        if charisma:
            self.stat_block.charisma = charisma
        return self

    def set_saving_throw_proficiencies(
        self,
        strength: bool | None = None,
        dexterity: bool | None = None,
        constitution: bool | None = None,
        intelligence: bool | None = None,
        wisdom: bool | None = None,
        charisma: bool | None = None,
        *abilities: Ability,
    ) -> Self:
        if self.stat_block.saving_throw_proficiencies:
            add_prof = set(self.stat_block.saving_throw_proficiencies)
        else:
            add_prof = set()

        add_prof.update(abilities)

        del_prof = set()

        def manage(ability: Ability, to_add: bool | None):
            if to_add is None:
                return
            if to_add:
                add_prof.add(ability)
            else:
                del_prof.add(ability)

        manage(Ability.STR, strength)
        manage(Ability.DEX, dexterity)
        manage(Ability.CON, constitution)
        manage(Ability.INT, intelligence)
        manage(Ability.WIS, wisdom)
        manage(Ability.CHA, charisma)

        prof = add_prof.difference(del_prof)
        self.stat_block.saving_throw_proficiencies = prof

        return self

    def add_skill_proficiencies(self, *skills: Skill) -> Self:
        if self.stat_block.skill_proficiencies is not None:
            sp = set(self.stat_block.skill_proficiencies)
        else:
            sp = set()

        sp.update(skills)
        self.stat_block.skill_proficiencies = sp
        return self

    def set_speed(self, speed: Speed | int | None) -> Self:
        if speed is not None:
            if not isinstance(speed, Speed):
                speed = Speed(speed)
            self.stat_block.speed = speed
        return self

    def infer_speed(self) -> None:
        speed = self.stat_block.speed
        if speed:
            return

        v: int | None = None
        size = self.stat_block.size
        if size in {Size.TINY, Size.SMALL}:
            v = 20
        elif size == Size.MEDIUM:
            v = 30
        elif size in {Size.LARGE, Size.HUGE, Size.GARGANTUAN}:
            v = 40

        if v is None:
            return

        self.set_speed(Speed(v))

    def set_size(self, size: Size | None):
        if size:
            self.stat_block.size = size
        return self

    def set_level(self, level: int | None) -> Self:
        if level:
            self.level = level
        return self

    def add_senses(self, *senses: Sense) -> Self:
        if self.stat_block.senses:
            curr_senses = list(self.stat_block.senses)
        else:
            curr_senses = []

        curr_senses.extend(senses)
        self.stat_block.senses = tuple(curr_senses)
        return self

    def add_languages(self, *languages: str) -> Self:
        if self.stat_block.languages:
            curr_lg = list(self.stat_block.languages)
        else:
            curr_lg = []

        curr_lg.extend(languages)
        self.stat_block.languages = tuple(curr_lg)
        return self

    def set_challenge_rating(self, cr: str | None) -> Self:
        if cr:
            self.stat_block.challenge_rating = cr
        return self

    def add_abilities(self, *args: PassiveAbility, **kwargs: str) -> Self:
        curr_abilities = self.stat_block.abilities
        if curr_abilities:
            curr_abilities = list(curr_abilities)
        else:
            curr_abilities = []

        curr_abilities.extend(args)
        curr_abilities.extend(
            PassiveAbility(key, value) for key, value in kwargs.items()
        )
        self.stat_block.abilities = tuple(curr_abilities)
        return self

    def add_actions(self, *actions: Action) -> Self:
        if self.stat_block.actions:
            curr_actions = list(self.stat_block.actions)
        else:
            curr_actions = []

        curr_actions.extend(actions)
        self.stat_block.actions = tuple(curr_actions)
        return self

    def add_action(
        self,
        name: str,
        description: str,
        category: str | None = None,
    ) -> Self:
        return self.add_actions(Action(name, description, category))

    def apply_racial_traits(
        self,
        race: Race,
    ) -> Self:
        self.set_size(race.size)
        self.set_type(race.type)
        self.set_speed(race.speed)
        return self

    def clone(self) -> StatBlockBuilder:
        return deepcopy(self)

    def create(self) -> StatBlock:
        self.infer_armor_class()
        self.infer_init_bonus()
        self.infer_max_hit_points()
        self.infer_passive_perception()
        self.infer_proficiency_bonus()
        self.infer_speed()
        return self.clone().stat_block
