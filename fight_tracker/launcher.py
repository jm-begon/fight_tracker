from .dice import RNG
from .encounter import Encounter
from .rendering import Narrator, StreamRenderer


class Game(object):
    @classmethod
    def init(cls, seed=None, renderer=None, narrator_factory=None):
        rng = RNG(seed)

        if narrator_factory is None:
            narrator_factory = Narrator

        if renderer is None:
            renderer = StreamRenderer()

        narrator = narrator_factory(renderer)
        game = cls(rng, narrator)

        def reg(creature, init=None):
            game.register(creature)
            game.encounter.add(creature, init)

        narrator.hello()

        return game, reg

    def __init__(self, rng, narrator, *encounters):
        self.rng = rng
        self.narrator = narrator
        self.encounters = list(encounters)
        if len(self.encounters) == 0:
            self.new_encounter()

    @property
    def renderer(self):
        return self.narrator.renderer

    @property
    def encounter(self):
        return self.encounters[-1]

    def register(self, *observables):
        for obs in observables:
            obs.add_observer(self.narrator)

    def new_encounter(self):
        encounter = Encounter()
        self.encounters.append(encounter)
        self.register(encounter)
        return encounter
