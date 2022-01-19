import sys
from random import Random

from .damage import Damage
from .events.attacks import Damaged, Healed
from .dice import RNG
from .events.base import MessageEvent
from .narrator import ConsoleNarrator
from .util import CircularQueue, Observable, ObserverMixin


class Participant(object):
    def __init__(self, creature, encounter, initiative):
        super().__init__()
        self.creature = creature
        self.initiative = initiative
        self.encounter = encounter

    @property
    def name(self):
        return self.creature.name

    def __repr__(self):
        return "{}({}, {}, {})".format(self.__class__.__name__,
                                       repr(self.creature),
                                       repr(self.encounter),
                                       repr(self.initiative))

    def can_act(self):
        # TODO return event?
        return not self.creature.is_ko


class Encounter(object):
    def __init__(self, logger):
        super().__init__()
        self.round = 0
        self.turn = 0
        self.queue = CircularQueue((lambda p: p.initiative))
        self.logger = logger

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)

    def add(self, creature, initiative=None):
        if initiative is None:
            initiative = 10  # TODO

        creature.add_observer(self.logger)

        initiative = int(initiative)  # for rolls
        participant = Participant(creature, self, initiative)
        self.queue.add(participant)
        return participant

    def __iter__(self):
        for p in self.queue:
            yield p

    def log_trigger(self, event):
        self.logger.update(event)
        event()

    def next_turn(self):
        self.turn += 1
        if self.queue.is_first():
            self.round += 1
            self.turn = 0
            self.log_trigger(MessageEvent("Start round {}".format(self.round))())

        participant = self.queue()
        if participant.can_act():
            self.log_trigger(MessageEvent("{} is ready to play".format(participant.name)))
            return participant.creature

        else:
            self.log_trigger(MessageEvent("{} cannot play".format(participant.name))())
            return self.next_turn()

    def start(self):
        self.queue.reset_head()
        return self.next_turn()



def encounter_factory(seed=None, narrator=None):
    """

    :param seed:
    :param narrator_factory:
    :return: (encounter, rng, trigger)
    """
    from . import Trigger

    if narrator is None:
        narrator = ConsoleNarrator()
    narrator.hello()
    rng = RNG(seed)

    return Encounter(narrator), rng, Trigger()
