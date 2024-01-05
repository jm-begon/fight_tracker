from __future__ import annotations

from abc import abstractmethod
from random import Random
from typing import Any, Dict, Literal, Union

# TODO context_manager for advantage and disadvantage ?
from .arithmetic import BaseIntable
from .typing import Intable

RNGLike = Union[int, Literal["expectation"], "BaseDrawer"]


class BaseDrawer:
    @abstractmethod
    def draw(self, maximum_value: int, sum_n: int = 1) -> int:
        raise NotImplementedError()


class Drawer(BaseDrawer):
    def __init__(self, seed: int | None = None) -> None:
        self.gen = Random(seed)

    def draw(self, maximum_value: int, sum_n: int = 1) -> int:
        return sum(self.gen.randint(1, maximum_value) for _ in range(sum_n))


class Expectation(BaseDrawer):
    def draw(self, maximum_value: int, sum_n: int = 1) -> int:
        return (sum_n * (maximum_value + 1)) // 2


class RNG:
    __instances__: Dict[Any, BaseDrawer] = {}

    @classmethod
    def get(
        cls,
        seed: RNGLike | None = None,
    ) -> BaseDrawer:
        if isinstance(seed, BaseDrawer):
            return seed
        inst = cls.__instances__.get(seed)
        if inst is None:
            if seed == "expectation":
                inst = Expectation()
            else:
                inst = Drawer(seed)
            cls.__instances__[seed] = inst
        return inst


class Dice(BaseIntable):
    @classmethod
    def expectation(cls, sides: int) -> Dice:
        return cls(sides, rng="expectation")

    def __init__(self, sides, rng: RNGLike | None = None):
        self.sides = sides
        self.n_dices = 1
        self.rng = RNG.get(rng)

    def __int__(self):
        return self.rng.draw(self.sides, self.n_dices)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.sides)}, " f"{repr(self.rng)})"

    def __str__(self):
        n_dices_str = "" if self.n_dices == 1 else str(self.n_dices)
        return f"{n_dices_str}d{self.sides}"

    def __mul__(self, factor: int) -> Dice:
        from copy import copy

        clone = copy(self)
        clone.n_dices = factor
        return clone

    def __rmul__(self, factor: int) -> Dice:
        return self.__mul__(factor)

    def roll(self) -> Roll:
        return Roll(self).set_value(int(self))


class D20(Dice):
    def __init__(self, rng=None):
        super().__init__(sides=20, rng=rng)
        # TODO manage adv/dis

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.rng)})"


class Roll(BaseIntable):
    @classmethod
    def outcome(cls, decorated: Intable) -> Roll:
        __o = cls(decorated)
        int(__o)
        return __o

    @classmethod
    def expected_outcome(
        cls, n_sided_dice: int, *others: Intable, n_dices: int = 1
    ) -> Roll:
        ans = n_dices * Dice.expectation(n_sided_dice)
        for __o in others:
            ans = ans + __o

        return cls.outcome(ans)

    def __init__(self, decorated):
        self.decorated = decorated
        self.value = None

    def set_value(self, v):
        self.value = v
        return self

    def unset(self):
        self.value = None
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

    def __str__(self):
        return f"{self.value} ({self.decorated})"
