import warnings

from fight_tracker.ability import Ability
from fight_tracker.damage import Damage
from fight_tracker.events import Damaged, Healed
from fight_tracker.events.base import MessageEvent
from fight_tracker.events.creature import HPEvent
from fight_tracker.util import Observable


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

        if new_hp < -self.hp_max:
            self.notify_hp(self._name("{} is dead"), p_event)
        if new_hp <= 0:
            self.notify_hp(self._name("{} is unconscious"), p_event)
        elif new_hp < tp:
            self.notify_hp(self._name("{} is in a critical state"), p_event)
        elif new_hp < half:
            self.notify_hp(self._name("{} is in bad shape"), p_event)

        self.set_hp(new_hp, p_event)

    def add_hp(self, delta, p_event=None):
        old_pv = self.hp
        new_hp = old_pv + delta
        if old_pv <= 0 < new_hp:
            pass  # TODO notif

        self.set_hp(new_hp, p_event)

    def set_hp(self, hp, p_event=None):
        self.hp = hp
        self.notify_hp(self._name("{} is now (HP)"),
                       p_event=p_event,
                       with_box=True)

    def notify_hp(self, message, p_event=None, with_box=False):
        event = HPEvent(self.creature, message, self)
        if with_box:
            event.render_hp_box = True
        if p_event:
            p_event.add_sub_events(event)
        else:
            self.notify(event)


class Creature(Observable):
    def __init__(self, name, armor_class, current_pv, pv_max=None):
        super().__init__()
        self.name = name
        self.armor_class = armor_class
        if pv_max is None:
            pv_max = current_pv
        self.pv_box = HpBox(self, current_pv, pv_max)
        self.misc = []
        self.saving_throws = {}

    @property
    def hp(self):
        return self.pv_box.hp

    @property
    def pv_max(self):
        return self.pv_box.hp_max

    @property
    def ac(self):
        return self.armor_class

    @property
    def is_ko(self):
        return self.hp <= 0

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
            if k not in Ability:
                warnings.warn("'{}' not an ability. Skipping".format(k))
            else:
                self.saving_throws[k] = v

    def __render__(self):
        return str(self)  # TODO




