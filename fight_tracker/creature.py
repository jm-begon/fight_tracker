import warnings

from .concept import Concept
from .arithmetic import DescriptiveTrue
from .mechanics.conditions import Dead, Unconscious, Incapacitated
from .mechanics.ability import Ability
from .mechanics.damage import Damage
from .events.event import MessageEvent, Conditioned, Damaged, Healed, HPEvent
from .mechanics.speed import Speed
from .rendering.misc import HPBar
from .util import Observable


class HpBox(Observable):
    def __init__(self, creature, hp, hp_max):
        super().__init__()
        self.creature = creature
        self.hp = hp
        self.hp_max = hp_max

    def _name(self, s):
        return s.format(self.creature.name)

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
            dc = max(delta//2,  10)
            bonus = self.creature.saving_throws.get(Ability.CON)
            bonus_str = "" if bonus is None else ", CON={:+d}".format(bonus)
            self.notify_hp(f"must succeed constitution saving throw"
                           f" (DC={dc}{bonus_str}) or lose concentration", p_event)

        self.set_hp(new_hp, p_event)

    def add_hp(self, delta, p_event=None):
        old_pv = self.hp
        new_hp = old_pv + delta
        if old_pv <= 0 < new_hp:
            pass  # TODO notif

        self.set_hp(new_hp, p_event)

    def set_hp(self, hp, p_event=None):
        self.hp = hp
        self.notify_hp(["is now at", self, "HP"],
                       p_event=p_event)

    def notify_hp(self, message, p_event=None):
        event = HPEvent(self.creature, message, self)
        self.notify(event, p_event)

    def __render__(self):
        return HPBar(self.hp, self.hp_max)


class Creature(Concept, Observable):
    def __init__(self, name, armor_class, current_pv, pv_max=None,
                 speed=30):
        super().__init__()
        self.name = name
        self.armor_class = armor_class
        if pv_max is None:
            pv_max = current_pv
        self.pv_box = HpBox(self, current_pv, pv_max)
        self._speed = speed if isinstance(speed, Speed) else Speed(speed)
        self.misc = []
        self.ability_modifiers = {}
        self.saving_throws = {}
        self.concentration = False
        self.conditions = set()
        self.vulnerabilities = set()  # condition or dmg types
        self.immunities = set()  # condition or dmg types
        self.resistances = set()

    @property
    def hp(self):
        return self.pv_box.hp

    @property
    def hp_max(self):
        return self.pv_box.hp_max

    @property
    def ac(self):
        return self.armor_class

    @property
    def initiative_bonus(self):
        return self.ability_modifiers.get(Ability.DEX, 0)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed_value):
        self._speed = speed_value if isinstance(speed_value, Speed) \
            else Speed(speed_value)

    def __repr__(self):
        return "{cls}(name={name}, armor_class={ca}, current_pv={pv}, " \
               "pv_max={pv_max})".format(cls=self.__class__.__name__,
                                         name=repr(self.name),
                                         ca=repr(self.armor_class),
                                         pv=repr(self.hp),
                                         pv_max=repr(self.hp_max))

    def set_saving_throws(self, **kwargs):
        for k, v in kwargs.items():
            ability = Ability[k]
            if ability is None:
                warnings.warn("'{}' not an ability. Skipping".format(k))
            else:
                self.saving_throws[ability] = v
        return self

    def set_ability_modifier(self, **kwargs):
        for k, v in kwargs.items():
            ability = Ability[k]
            if ability is None:
                warnings.warn("'{}' not an ability. Skipping".format(k))
            else:
                self.ability_modifiers[ability] = v
        return self

    def add_observer(self, observer):
        super(Creature, self).add_observer(observer)
        self.pv_box.add_observer(observer)

    def short_repr(self):
        return self.name

    def mid_repr(self):
        return repr(self)

    # def long_repr(self):
    #     return StatBlock()

    def __sub__(self, damage):
        if isinstance(damage, int):
            value = damage
            damage = Damage(value)
        else:
            value = int(damage)

        if value < 0:
            return self.__add__(damage)

        if damage.dtype in self.resistances:
            damage.is_resisted = True
        if damage.dtype in self.immunities:
            damage.is_immuned = True
        if damage.dtype in self.vulnerabilities:
            damage.is_weakness = True

        event = Damaged(self, damage, self)
        self.pv_box.remove_hp(int(event), p_event=event)
        self.notify(event)

        return self

    def __add__(self, other):
        value = int(other)
        if value < 0:
            return self.__sub__(other)

        event = Healed(self, other, self)

        self.pv_box.remove_hp(int(event), p_event=event)
        self.notify(event)
        return self

    def add_misc(self, text):
        # TODO move to block stat?
        self.misc.append(text)
        return self

    def do_concentrate_on(self, boolable):  # for repr purposes
        self.concentration = boolable
        return self

    def do_stop_concentrating(self):
        self.concentration = False
        return self

    def concentrate_on(self, something, p_event=None):
        self.do_concentrate_on(DescriptiveTrue(something))
        self.notify(
            MessageEvent(self, ["is concentrating on", something], self),
            p_event
        )

        return self.stop_concentrating

    def stop_concentrating(self, p_event=None):
        self.do_stop_concentrating()
        self.notify(
            MessageEvent(self, "is no longer concentrating", self),
            p_event
        )

    @property
    def is_concentrating(self):
        return bool(self.concentration)

    def do_add_conditions(self, *conditions):  # for repr purposes
        self.conditions.update(conditions)
        return self

    def add_condition(self, condition, p_event=None):
        self.do_add_conditions(condition)

        event = Conditioned(self, condition, self)
        self.notify(event, p_event)

        if self.is_concentrating and isinstance(condition, Incapacitated):
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

    def can_act(self):
        move = True
        take_act = True
        for condition in self.conditions:
            move = move and condition.can_move()
            take_act = take_act and condition.can_take_action()

        return move or take_act


class PlayerCharacter(Creature):
    def __init__(self, player, name, armor_class, current_pv, pv_max=None,
                 speed=30):
        super(PlayerCharacter, self).__init__(name, armor_class, current_pv, 
                                              pv_max=pv_max, speed=speed)
        self.player = player

    # TODO add comment regarding death saves? Problem for nesting events
    # def add_condition(self, condition, p_event=None):
    #     remove_fn = super().add_condition(condition, p_event)
    #     if isinstance(condition, Unconscious):
    #         self.notify(MessageEvent(self, [], self))
    #     return remove_fn


class NPC(Creature):
    pass  # TODO
        



