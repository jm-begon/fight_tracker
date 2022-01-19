from enum import Enum


class DamageType(Enum):
    PIERCING = "piercing"


class Damage(object):
    def __init__(self, raw, dtype=None):
        self.raw_dmg = int(raw)  # transform roll into value
        self.dtype = dtype
        self.is_resisted = False
        self.is_immuned = False

    def __int__(self):
        if self.is_immuned:
            return 0
        if self.is_resisted:
            return self.raw_dmg // 2
        return self.raw_dmg

    def __str__(self):
        type_str = "" if self.dtype is None else "{} ".format(self.dtype.value)
        s = "{} point(s) of {}damage".format(int(self), type_str)
        if self.is_immuned:
            return "{} (immune)".format(s)
        if self.is_resisted:
            return "{} (resistance, half-damage)".format(s)
        return s


class Piercing(Damage):
    def __init__(self, raw):
        super(Piercing, self).__init__(raw, dtype=DamageType.PIERCING)