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
    def draw(self, maximum_value: int) -> int:
        raise NotImplementedError()


class Drawer(BaseDrawer):
    def __init__(self, seed: int | None = None) -> None:
        self.gen = Random(seed)

    def draw(self, maximum_value: int) -> int:
        return self.gen.randint(1, maximum_value)


class Expectation(BaseDrawer):
    def draw(self, maximum_value: int) -> int:
        return (maximum_value + 1) // 2


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
    def __init__(self, sides, rng: RNGLike | None = None):
        self.sides = sides
        self.n_dices = 1
        self.rng = RNG.get(rng)

    def __int__(self):
        ans = 0
        for _ in range(self.n_dices):
            ans += self.rng.draw(self.sides)
        return ans

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


class D20(Dice):
    def __init__(self, rng=None):
        super(D20, self).__init__(sides=20, n_dices=1, rng=rng)
        # TODO manage adv/dis

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.rng)})"


class Roll(BaseIntable):
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
