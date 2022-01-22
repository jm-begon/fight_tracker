from .creature import Creature
from .dice import RNG
from .encounter import Encounter, Participant
from .rendering.narrator import Narrator
from .rendering.stream_renderer.renderer import StreamRenderer


__all__ = ["Creature", "Encounter", "Participant", "encounter_factory",
           ]



def encounter_factory(seed=None, renderer=None):
    """

    :param seed:
    :param narrator_factory:
    :return: (encounter, rng, trigger)
    """
    if renderer is None:
        renderer = StreamRenderer()
    narrator = Narrator(renderer)
    narrator.hello()
    rng = RNG(seed)

    return Encounter(narrator), rng, renderer
