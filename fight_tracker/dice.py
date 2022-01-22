from random import Random

# TODO context_manager for advantage and disadvantage


class RNG(object):
    def __init__(self, seed):
        self.gen = Random(seed)
        self.advantage = 0
        self.disadvantage = 0


class Dice(object):
    def __init__(self, sides, rng=None):
        self.sides = sides
        if rng is None or isinstance(rng, int):
            rng = RNG(rng)
        self.rng = rng


class Roll(object):
    # Lazy
    pass


