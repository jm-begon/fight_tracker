from .dice import RNG
from .events.base import MessageEvent
from .rendering.table import Table, BoolCell
from .util import CircularQueue


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
        # Careful, actual moves the queue
        for p in self.queue:
            yield p

    def log_message(self, message):
        self.logger.log(MessageEvent(message))  # TODO class ? (for isinstance)

    def get_next_participant(self):
        next_participant = None
        for j in range(1, len(self.queue) - 1):
            next_participant = self.queue.peek(j)
            if next_participant.can_act():
                break
            else:
                next_participant = None
        return next_participant

    def next_turn(self):
        participant = self.queue()
        self.turn += 1
        if self.queue.is_first():
            self.round += 1
            self.turn = 0
            self.log_message("Start round {}".format(self.round))

        if participant.can_act():
            next_participant = self.get_next_participant()
            next_str = ""
            if next_participant is not None:
                next_str = " (next in line is {})".format(next_participant.name)
            self.log_message("{} is ready to play{}".format(participant.name, next_str))

            return participant.creature

        else:
            self.log_message("{} cannot play".format(participant.name))
            return self.next_turn()

    def start(self):
        self.log_message("Battle begins!")
        self.queue.reset_head()
        return self.next_turn()

    def end(self):
        self.log_message("Battle is over")

    def __render__(self, renderer):
        curr = self.queue.head
        table = Table(header=True)
        table.fill_row("Curr.", "Init.", "Participant", "AC", "HP/HP max")

        for i, participant in enumerate(self.queue.list_in_order()):
            creature = participant.creature
            table.fill_cell(BoolCell(i == curr))
            table.fill_cell(participant.initiative)
            table.fill_cell(participant.name)
            table.fill_cell(creature.pv_box)
            table.fill_cell(creature.armor_class, new_column=False)
            # TODO saving throws
            # TODO quid conditions, concentration?

            table.new_row()

        table.delete_row()

        renderer(table)



