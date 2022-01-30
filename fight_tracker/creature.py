import warnings

from .mechanics.conditions import Dead, Unconscious
from .events.conditions import Conditioned
from .mechanics.ability import Ability
from .mechanics.damage import Damage
from .events import Damaged, Healed
from .events.creature import HPEvent
from .concept import Concept
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
        print()

        if new_hp <= -self.hp_max:
            self.creature.add_condition(Dead(), p_event)
        if new_hp <= 0:
            self.creature.add_condition(Unconscious(), p_event)
        elif new_hp < tp:
            self.notify_hp("is in a critical state", p_event)
        elif new_hp < half:
            self.notify_hp("is in bad shape", p_event)

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


class Creature(Concept, Observable):
    def __init__(self, name, armor_class, current_pv, pv_max=None):
        super().__init__()
        self.name = name
        self.armor_class = armor_class
        if pv_max is None:
            pv_max = current_pv
        self.pv_box = HpBox(self, current_pv, pv_max)
        self.misc = []
        self.saving_throws = {}
        self.conditions = set()

    @property
    def hp(self):
        return self.pv_box.hp

    @property
    def pv_max(self):
        return self.pv_box.hp_max

    @property
    def ac(self):
        return self.armor_class

    def __repr__(self):
        return "{cls}(name={name}, armor_class={ca}, current_pv={pv}, " \
               "pv_max={pv_max})".format(cls=self.__class__.__name__,
                                         name=repr(self.name),
                                         ca=repr(self.armor_class),
                                         pv=repr(self.hp),
                                         pv_max=repr(self.pv_max))

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
        # if value == 0:
        #     return self.notify_apply(NoOp())
        if value < 0:
            return self.__add__(damage)

        event = Damaged(self, damage, self)
        self.pv_box.remove_hp(int(event), p_event=event)
        self.notify(event)

        # TODO check for resistances/immunities and adapt damage
        # TODO handle concentration ?
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
        self.misc.append(text)
        return self

    def set_saving_throws(self, **kwargs):
        for k, v in kwargs.items():
            ability = Ability[k]
            if ability is None:
                warnings.warn("'{}' not an ability. Skipping".format(k))
            else:
                self.saving_throws[ability] = v
        return self

    def add_conditions(self, *conditions):
        self.conditions.union(conditions)
        return self

    def add_condition(self, condition, p_event=None):
        self.add_conditions(condition)

        event = Conditioned(self, condition, self)
        self.notify(event, p_event)

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






