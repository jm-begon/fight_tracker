from fight_tracker.mechanics.damage import Damage
from .base import TargetedEvent


class Attacked(TargetedEvent):
    pass


class Hit(TargetedEvent):
    pass


class Missed(TargetedEvent):
    pass


class Damaged(TargetedEvent):
    def __init__(self, target, damage, source):
        super().__init__(target, source)
        if isinstance(damage, int):
            damage = Damage(damage)
        self.damage = damage

    def __str__(self):
        return self.add_source_str("{} takes {}".format(self.target.name, self.damage))

    def __int__(self):
        return int(self.damage)

    def __render_self_event__(self):
        return ["takes", self.damage]


class Healed(TargetedEvent):
    def __init__(self, target, bonus, source):
        super().__init__(target, source)
        self.bonus = bonus

    def __str__(self):
        return self.add_source_str("{} regains {} hit point(s)"
                                   "".format(self.target.name, int(self.bonus)))

    def __int__(self):
        return int(self.bonus)

    def __render_self_event__(self):
        return [f"regains {int(self.bonus)} hit point(s)"]


class HPEvent(TargetedEvent):
    def __init__(self, target, message, source):
        super(HPEvent, self).__init__(target, source)
        self.message = message

    def __constructor_repr__(self):
        return "{}({}, {}, {})".format(self.__class__.__name__,
                                       repr(self.target),
                                       repr(self.message),
                                       repr(self.source))

    def __render_self_event__(self):
        if isinstance(self.message, str):
            return [self.message]
        return self.message
