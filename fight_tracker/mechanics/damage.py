from enum import Enum


class DamageType(Enum):
    ACID = "acid"
    BLUDGEONING = "bludgeoning"
    COLD = "cold"
    FIRE = "fire"
    FORCE = "force"
    LIGHTNING = "lightning"
    NECROTIC = "necrotic"
    PIERCING = "piercing"
    POISON = "poison"
    PSYCHIC = "psychic"
    RADIANT = "radiant"
    SLASHING = "slashing"
    THUNDER = "thunder"

    @classmethod
    def __getitem__(cls, item):
        if item is None:
            return None

        if isinstance(item, cls):
            return item
        for type_ in cls:
            if item == type_.value or type_.name:
                return type_

        return None


class Damage(object):
    @classmethod
    def as_type(cls, raw, type_str):
        return cls(raw, DamageType[type_str.upper()])

    def __init__(self, raw, dtype=None):
        self.raw_dmg = int(raw)  # transform roll into value
        self.dtype = dtype
        self.is_resisted = False
        self.is_immuned = False
        self.is_weakness = False

    def __int__(self):
        dmg = self.raw_dmg
        if self.is_weakness:
            dmg *= 2
        if self.is_resisted:
            dmg //= 2
        if self.is_immuned:
            dmg = 0
        return dmg

    def __str__(self):
        type_str = "" if self.dtype is None else "{} ".format(self.dtype.value)
        s = "{} point(s) of {}damage".format(int(self), type_str)
        if self.is_immuned:
            return "{} (immune)".format(s)
        if self.is_resisted:
            return "{} (resistance, half damage)".format(s)
        if self.is_resisted:
            return "{} (vulnerabilities, double damage)".format(s)
        return s
