from random import Random

# TODO context_manager for advantage and disadvantage

class RNG:
    __instances__ = {}

    @classmethod
    def get(cls, seed=None):
        inst = cls.__instances__.get(seed)
        if inst is None:
            inst = cls(seed)
            cls.__instances__[seed] = inst
        return inst

    def __init__(self, seed):
        self.gen = Random(seed)

    def draw(self, maximum_value):
        return self.gen.randint(1, maximum_value)


class Intable:
    def __int__(self):
        return 0

    def __add__(self, other):
        return Addition(self, other)

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class Addition(Intable):
    def __init__(self, *intables):
        self.intables = list(intables)

    def __int__(self):
        return sum(int(i) for i in self.intables)

    def __repr__(self):
        return f"{self.__class__.__name__}(*{repr(self.intables)})"


class Subtraction(Intable):
    def __init__(self, left_operand, right_operand):
        self.left = left_operand
        self.right = right_operand

    def __int__(self):
        return int(self.left) - int(self.right)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.left)}, " \
               f"{repr(self.right)})"


class Dice(Intable):
    def __init__(self, sides, rng=None):
        self.sides = sides
        if rng is None or isinstance(rng, int):
            rng = RNG.get(rng)
        self.rng = rng

    def __int__(self):
        return self.rng.draw(self.sides)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.sides)}, " \
               f"{repr(self.rng)})"


class D20(Dice):
    def __init__(self, rng=None):
        super(D20, self).__init__(sides=20, rng=rng)
        # TODO manage adv/dis

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.rng)})"


class Roll(Intable):
    def __init__(self, decorated):
        self.decorated = decorated
        self.value = None

    def set_value(self, v):
        self.value = v
        return self

    def __int__(self):
        if self.value is None:
            self.set_value(int(self.decorated))
        return self.value

    def __repr__(self):
        s = f"{self.__class__.__name__}({repr(self.decorated)})"
        if self.value is not None:
            s += f".set_value({self.value})"
        return s
