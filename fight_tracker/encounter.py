from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from .creature import NPC, Creature, PlayerCharacter
from .dice import D20, Roll
from .events.event import (
    EncounterEnd,
    EncounterEvent,
    EncounterStart,
    NewRound,
    TurnEvent,
)
from .mechanics.ability import Ability
from .rendering.table import BoolCell, Table
from .typing import Intable
from .util import CircularQueue, Observable


@dataclass
class Participant:
    creature: Creature
    encounter: Encounter
    initiative: int

    @property
    def name(self) -> str:
        return self.creature.nickname


class Encounter(Observable):
    def __init__(self):
        super().__init__()
        self.round = 0
        self.turn = 0
        self.queue = CircularQueue((lambda p: p.initiative))

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)

    def add(self, creature: Creature, initiative: Intable | None = None):
        if initiative is None:
            initiative = Roll(D20() + creature.initiative_bonus)

        participant = Participant(creature, self, int(initiative))
        self.queue.add(participant)

        self.notify(
            EncounterEvent([creature, f"roll a {initiative}" f" as initiative"], self)
        )
        return participant

    def __iter__(self):
        # Careful, actual moves the queue
        for p in self.queue:
            yield p

    def get_next_participant(self):
        next_participant = None
        for j in range(1, len(self.queue) - 1):
            next_participant: Participant = self.queue.peek(j)
            if next_participant.creature.can_play():
                break
            else:
                next_participant = None
        return next_participant

    def next_turn(self):
        participant: Participant = self.queue()
        self.turn += 1
        turn_event = TurnEvent(participant, self)

        if self.queue.is_first():
            self.round += 1
            self.turn = 0
            NewRound(self.round, self).notify()

        if participant.creature.can_play():
            next_participant = self.get_next_participant()
            if next_participant is not None:
                turn_event.add_next(next_participant).notify()
            return participant.creature

        else:
            turn_event.disable().notify()
            # TODO differentiate between cannot move and cannot act?
            if not isinstance(participant.creature, NPC):
                return self.next_turn()

    def start(self):
        EncounterStart(self).notify()
        self.queue.reset_head()
        return self.next_turn()

    def end(self):
        EncounterEnd(self).notify()
        return self

    def __render__(self):
        curr = self.queue.head
        table = Table(header=True)
        table.fill_row(
            "Curr.",
            "Init.",
            "Participant",
            "HP",
            "AC",
            *[ability.name for ability in Ability],
            "Concentration",
            "Conditions",
        )

        for i, participant in enumerate(self.queue.list_in_order()):
            participant = cast(Participant, participant)
            creature = participant.creature
            table.fill_cell(BoolCell(i == curr))
            table.fill_cell(participant.initiative)
            if isinstance(creature, PlayerCharacter):
                table.fill_cell((creature, f"({creature.nickname})"))
            else:
                table.fill_cell((creature.nickname, "(", creature, ")"))
            table.fill_cell(creature.hp_box)
            table.fill_cell(int(creature.armor_class))  # Remove description
            for ability in Ability:
                save = participant.creature.saving_throws.get(ability)
                if save is None:
                    table.fill_cell("-")
                else:
                    table.fill_cell("{:+d}".format(int(save)))

            table.fill_cell(BoolCell(creature.is_concentrating))
            table.fill_cell(list(participant.creature.list_conditions()))

            table.delete_cell().new_row()

        table.delete_row()

        return table

    def __add__(self, __o: int) -> Encounter:
        for _ in range(__o):
            self.next_turn()

        return self
