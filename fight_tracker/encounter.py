from fight_tracker.mechanics.ability import Ability
from .events.encounter import NewRound, TurnEvent, EncounterStart, EncounterEnd
from .rendering.table import Table, BoolCell
from .util import CircularQueue, Observable


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


class Encounter(Observable):
    def __init__(self):
        super().__init__()
        self.round = 0
        self.turn = 0
        self.queue = CircularQueue((lambda p: p.initiative))

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)

    def add(self, creature, initiative=None):
        if initiative is None:
            initiative = 10  # TODO

        initiative = int(initiative)  # for rolls
        participant = Participant(creature, self, initiative)
        self.queue.add(participant)
        return participant

    def __iter__(self):
        # Careful, actual moves the queue
        for p in self.queue:
            yield p

    def get_next_participant(self):
        next_participant = None
        for j in range(1, len(self.queue) - 1):
            next_participant = self.queue.peek(j)
            if next_participant.creature.can_act():
                break
            else:
                next_participant = None
        return next_participant

    def next_turn(self):
        participant = self.queue()
        self.turn += 1
        turn_event = TurnEvent(participant, self)

        if self.queue.is_first():
            self.round += 1
            self.turn = 0
            NewRound(self.round, self).notify()

        if participant.creature.can_act():
            next_participant = self.get_next_participant()
            if next_participant is not None:
                turn_event.add_next(next_participant).notify()
            return participant.creature

        else:
            turn_event.disable().notify()
            return self.next_turn()

    def start(self):
        EncounterStart(self).notify()
        self.queue.reset_head()
        return self.next_turn()

    def end(self):
        EncounterEnd(self).notify()

    def __render__(self):
        curr = self.queue.head
        table = Table(header=True)
        table.fill_row("Curr.", "Init.", "Participant", "HP", "AC",
                       *[ability.name for ability in Ability],
                       "Conditions")

        for i, participant in enumerate(self.queue.list_in_order()):
            creature = participant.creature
            table.fill_cell(BoolCell(i == curr))
            table.fill_cell(participant.initiative)
            table.fill_cell(participant.creature)
            table.fill_cell(creature.pv_box)
            table.fill_cell(creature.armor_class)
            for ability in Ability:
                save = participant.creature.saving_throws.get(ability)
                if save is None:
                    table.fill_cell("n/a")
                else:
                    table.fill_cell("{:+d}".format(int(save)))
            table.fill_cell(list(participant.creature.list_conditions()))
            # TODO concentration?
            table.delete_cell().new_row()



        table.delete_row()

        return table



