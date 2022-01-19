from fight_tracker.damage import Damage
from .base import TargetedEvent


class Attacked(TargetedEvent):
    pass


class Hit(TargetedEvent):
    pass


class Missed(TargetedEvent):
    pass


class Damaged(TargetedEvent):
    def __init__(self, target, damage, callback, source=None):
        super().__init__(target, source)
        if isinstance(damage, int):
            damage = Damage(damage)
        self.damage = damage
        self.callback = callback

    def __str__(self):
        return self.add_source("{} takes {}".format(self.target.name, self.damage))

    def __call__(self, *args, **kwargs):
        # TODO check for resistance/immunities
        self.callback(self)

    def __int__(self):
        return int(self.damage)


class Healed(TargetedEvent):
    def __init__(self, target, bonus, callback, source=None):
        super().__init__(target, source)
        self.bonus = bonus
        self.callback = callback

    def __str__(self):
        return self.add_source("{} regains {} hit point(s)"
                               "".format(self.target.name, int(self.bonus)))

    def __int__(self):
        return int(self.bonus)
