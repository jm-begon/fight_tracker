from __future__ import annotations

from typing import Self

from .dice import RNG
from .encounter import Encounter
from .rendering import Narrator, StreamRenderer
from .typing import Intable


class Game(object):
    @classmethod
    def init(cls, seed=None, renderer=None, narrator_factory=None) -> Game:
        rng = RNG.get(seed)

        if narrator_factory is None:
            narrator_factory = Narrator

        if renderer is None:
            renderer = StreamRenderer()

        narrator = narrator_factory(renderer)
        game = cls(rng, narrator)

        narrator.hello()

        return game

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

    def populate_encounter(self) -> EncounterBuilder:
        return EncounterBuilder(self)

    def create_encounter(self) -> EncounterBuilder:
        self.new_encounter()
        return self.populate_encounter()


class EncounterBuilder:
    def __init__(self, game: Game) -> None:
        self.game = game

    def add(self, creature, initiative: Intable | None = None) -> Self:
        self.game.register(creature)
        self.game.encounter.add(creature, initiative)
        return self

    def start(self) -> Encounter:
        e = self.game.encounter
        e.start()
        return e
