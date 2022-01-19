from fight_tracker.damage import Damage
from fight_tracker.events import Damaged, Healed
from fight_tracker.events.base import MessageEvent
from fight_tracker.util import Observable


class PvBox(Observable):
    def __init__(self, creature, pv, pv_max):
        super().__init__()
        self.creature = creature
        self.pv = pv
        self.pv_max = pv_max

    def remove_pv(self, delta):
        half = self.pv_max // 2
        tp = self.pv_max // 10
        old_pv = self.pv
        self.pv = old_pv - delta
        if self.pv <= 0:
            self.notify_trigger(MessageEvent("{} is unconscious ({}/{})".format(self.creature.name, self.pv, self.pv_max)))
        elif self.pv < tp < old_pv:
            self.notify_trigger(MessageEvent("{} is in a critical state ({}/{})".format(self.creature.name, self.pv, self.pv_max)))
        elif self.pv < half < old_pv:
            self.notify_trigger(MessageEvent("{} is in bad shape ({}/{})".format(self.creature.name, self.pv, self.pv_max)))

    def add_pv(self, delta):
        old_pv = self.pv
        self.pv = old_pv + delta
        if old_pv <= 0 < self.pv:
            pass  # TODO notif


class Creature(Observable):
    def __init__(self, name, armor_class, current_pv, pv_max=None):
        super().__init__()
        self.name = name
        self.armor_class = armor_class
        if pv_max is None:
            pv_max = current_pv
        self.pv_box = PvBox(self, current_pv, pv_max)

    @property
    def pv(self):
        return self.pv_box.pv

    @property
    def pv_max(self):
        return self.pv_box.pv_max

    @property
    def ac(self):
        return self.armor_class

    @property
    def is_ko(self):
        return self.pv <= 0

    def __repr__(self):
        return "{cls}(name={name}, armor_class={ca}, current_pv={pv}, " \
               "pv_max={pv_max})".format(cls=self.__class__.__name__,
                                         name=repr(self.name),
                                         ca=repr(self.armor_class),
                                         pv=repr(self.pv),
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

        def callback(event):
            self.notify(event)
            self.pv_box.remove_pv(int(event))

        return Damaged(self, damage, callback)

    def __add__(self, other):
        value = int(other)
        if value < 0:
            return self.__sub__(other)

        def callback(event):
            self.notify(event)
            self.pv_box.add_pv(int(event))

        return Healed(self, other, callback)


