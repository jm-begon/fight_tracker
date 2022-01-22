from fight_tracker.damage import Damage
from fight_tracker.events import Damaged, Healed
from fight_tracker.events.base import MessageEvent
from fight_tracker.util import Observable


class HpBox(Observable):
    def __init__(self, creature, hp, hp_max):
        super().__init__()
        self.creature = creature
        self.hp = hp
        self.hp_max = hp_max

    def remove_hp(self, delta):
        half = self.hp_max // 2
        tp = self.hp_max // 10
        old_pv = self.hp
        self.hp = old_pv - delta
        if self.hp <= 0:
            self.notify(MessageEvent("{} is unconscious ({}/{})".format(self.creature.name, self.hp, self.hp_max)))
        elif self.hp < tp < old_pv:
            self.notify(MessageEvent("{} is in a critical state ({}/{})".format(self.creature.name, self.hp, self.hp_max)))
        elif self.hp < half < old_pv:
            self.notify(MessageEvent("{} is in bad shape ({}/{})".format(self.creature.name, self.hp, self.hp_max)))
        # TODO auto-death

    def add_hp(self, delta):
        old_pv = self.hp
        self.hp = old_pv + delta
        if old_pv <= 0 < self.hp:
            pass  # TODO notif

    # TODO set_hp and notify current state


class Creature(Observable):
    def __init__(self, name, armor_class, current_pv, pv_max=None):
        super().__init__()
        self.name = name
        self.armor_class = armor_class
        if pv_max is None:
            pv_max = current_pv
        self.pv_box = HpBox(self, current_pv, pv_max)
        self.misc = []
        # TODO saves would be nice to go along AC

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

        event = Damaged(self, damage)
        self.notify(event)
        self.pv_box.remove_hp(int(event))

        # TODO check for resistances/immunities and adapt damage
        # TODO handle concentraiton ?
        return event

    def __add__(self, other):
        value = int(other)
        if value < 0:
            return self.__sub__(other)

        event = Healed(self, other)

        self.notify(event)
        self.pv_box.remove_hp(int(event))
        return event

    def add_misc(self, text):
        self.misc.append(text)
        return self



