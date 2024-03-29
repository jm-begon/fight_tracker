from __future__ import annotations

import warnings
from typing import Any, Dict, Set

from .arithmetic import DescriptiveTrue
from .concept import Concept
from .events.event import Conditioned, Damaged, Healed, HPEvent, MessageEvent
from .mechanics.ability import Ability
from .mechanics.conditions import Condition, Dead, Incapacitated, Unconscious
from .mechanics.damage import Damage
from .mechanics.speed import Speed
from .rendering.misc import HPBar
from .statblock import StatBlock
from .typing import Boolable, Intable
from .util import Observable


class HpBox(Observable):
    @classmethod
    def create(
        cls,
        creature: Creature,
        current_hp: Intable | None = None,
        hp_max: Intable | None = None,
    ) -> HpBox:
        if hp_max is None and current_hp is None:
            raise ValueError("HP needed to run a creature")
        elif hp_max is None:
            hp_max = current_hp
        if current_hp is None:
            current_hp = hp_max

        return cls(creature, int(current_hp), int(hp_max))  # type: ignore

    def __init__(self, creature: Creature, hp: int, hp_max: int):
        super().__init__()
        self.creature = creature
        self.hp = hp
        self.hp_max = hp_max

    def _name(self, s):
        return s.format(self.creature.nickname)

    def remove_hp(self, delta, p_event=None):
        half = self.hp_max // 2
        tp = self.hp_max // 10
        old_pv = self.hp
        new_hp = old_pv - delta

        if new_hp <= -self.hp_max:
            self.creature.add_condition(Dead(), p_event)
        if new_hp <= 0:
            self.creature.add_condition(Unconscious(), p_event)
        elif new_hp < tp:
            self.notify_hp("is in a critical state", p_event)
        elif new_hp < half:
            self.notify_hp("is in bad shape", p_event)

        if delta > 0 and self.creature.is_concentrating:
            dc = max(delta // 2, 10)
            bonus = self.creature.statblock.constitution_saving_throw
            bonus_str = "" if bonus is None else f", {bonus}"
            self.notify_hp(
                f"must succeed constitution saving throw"
                f" (DC={dc}{bonus_str}) or lose concentration",
                p_event,
            )

        self.set_hp(new_hp, p_event)

    def add_hp(self, delta, p_event=None):
        old_pv = self.hp
        new_hp = old_pv + delta
        if old_pv <= 0 < new_hp:
            pass  # TODO notif

        self.set_hp(new_hp, p_event)

    def set_hp(self, hp, p_event=None):
        self.hp = hp
        self.notify_hp(["is now at", self, "HP"], p_event=p_event)

    def notify_hp(self, message, p_event=None):
        event = HPEvent(self.creature, message, self)
        self.notify(event, p_event)

    def __render__(self):
        return HPBar(self.hp, self.hp_max)


class Creature(Concept, Observable):
    @classmethod
    def quick(
        cls,
        nickname: str,
        name: str,
        armor_class: Intable,
        hp_max: Intable,
        hp: int | None = None,
        speed: Speed | int | None = None,
        **kwargs: Any,
    ) -> Creature:
        if speed is None:
            speed = 30  # most common
        if not isinstance(speed, Speed):
            speed = Speed(speed)
        return cls(
            nickname=nickname,
            statblock=StatBlock(
                name=name,
                armor_class=armor_class,
                max_hit_points=hp_max,
                speed=speed,
                **kwargs,
            ),
            current_hp=hp,
        )

    def __init__(
        self,
        nickname: str,
        statblock: StatBlock,
        current_hp: int | None = None,
    ):
        super().__init__()
        self.nickname = nickname
        self._statblock = statblock
        self.hp_box = HpBox.create(self, current_hp, statblock.max_hit_points)
        self._speed = statblock.speed  # TODO quid None
        self.concentration: Boolable = False  # TODO impl. rules for concentation
        self.conditions: Set[Condition] = set()

        self.saving_throws: Dict = {}  # TODO remove

    @property
    def name(self) -> str:
        return self._statblock.name

    @property
    def statblock(self) -> StatBlock:
        return self._statblock

    @property
    def armor_class(self) -> int:
        x = self._statblock.armor_class
        if x is None:
            raise RuntimeError("Armor class needed to run a creature")
        return int(x)

    @property
    def hp(self) -> int:
        return self.hp_box.hp

    @property
    def hp_max(self) -> int:
        return self.hp_box.hp_max

    @property
    def ac(self):
        return self.armor_class

    @property
    def initiative_bonus(self) -> int:
        x = self.statblock.initiative_bonus
        return int(x) if x is not None else 0

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed_value):
        self._speed = (
            speed_value if isinstance(speed_value, Speed) else Speed(speed_value)
        )

    # def __repr__(self):
    #     return (
    #         "{cls}(name={name}, armor_class={ca}, current_pv={pv}, "
    #         "pv_max={pv_max})".format(
    #             cls=self.__class__.__name__,
    #             name=repr(self.name),
    #             ca=repr(self.armor_class),
    #             pv=repr(self.hp),
    #             pv_max=repr(self.hp_max),
    #         )
    #     )

    def add_observer(self, observer):
        super(Creature, self).add_observer(observer)
        self.hp_box.add_observer(observer)

    def short_repr(self):
        return self.name

    def mid_repr(self):
        return repr(self)

    def long_repr(self):
        from .rendering import StreamRenderer

        return StreamRenderer()(self._statblock)

    def __sub__(self, damage):
        if isinstance(damage, int):
            value = damage
            damage = Damage(value)
        else:
            value = int(damage)

        if value < 0:
            return self.__add__(damage)

        # TODO enable
        # if damage.dtype in self.resistances:
        #     damage.is_resisted = True
        # if damage.dtype in self.immunities:
        #     damage.is_immuned = True
        # if damage.dtype in self.vulnerabilities:
        #     damage.is_weakness = True

        event = Damaged(self, damage, self)
        self.hp_box.remove_hp(int(event), p_event=event)
        self.notify(event)

        return self

    def __add__(self, other):
        value = int(other)
        if value < 0:
            return self.__sub__(other)

        event = Healed(self, other, self)

        self.hp_box.remove_hp(int(event), p_event=event)
        self.notify(event)
        return self

    def do_concentrate_on(self, boolable: Boolable):  # for repr purposes
        self.concentration = boolable
        return self

    def do_stop_concentrating(self):
        self.concentration = False
        return self

    def concentrate_on(self, something, p_event=None):
        self.do_concentrate_on(DescriptiveTrue(something))
        self.notify(
            MessageEvent(self, ["is concentrating on", something], self), p_event
        )

        return self.stop_concentrating

    def stop_concentrating(self, p_event=None):
        self.do_stop_concentrating()
        self.notify(MessageEvent(self, "is no longer concentrating", self), p_event)

    @property
    def is_concentrating(self):
        return bool(self.concentration)

    def do_add_conditions(self, *conditions):  # for repr purposes
        self.conditions.update(conditions)
        return self

    def add_condition(self, condition: Condition, p_event=None):
        self.do_add_conditions(condition)

        event = Conditioned(self, condition, self)
        self.notify(event, p_event)

        if self.is_concentrating and not condition.can_concentrate():
            self.stop_concentrating(p_event)

        # TODO replace exhausted lvl6 by dead
        #      and remove everything (?) on dead

        def remove_condition():
            try:
                self.conditions.remove(condition)
            except KeyError:
                pass  # Already removed

        return remove_condition

    def list_conditions(self):
        return iter(self.conditions)

    def can_play(self):
        # TODO display
        move = True
        take_act = True
        for condition in self.conditions:
            move = move and condition.can_move()
            take_act = take_act and condition.can_take_action()

        return move or take_act


class PlayerCharacter(Creature):
    @property
    def player(self) -> str:
        return self.nickname

    # TODO add comment regarding death saves? Problem for nesting events
    # def add_condition(self, condition, p_event=None):
    #     remove_fn = super().add_condition(condition, p_event)
    #     if isinstance(condition, Unconscious):
    #         self.notify(MessageEvent(self, [], self))
    #     return remove_fn


class NPC(Creature):
    pass
