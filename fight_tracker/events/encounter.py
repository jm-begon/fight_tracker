from .base import Event


class EncounterEvent(Event):
    def __init__(self, message, source):
        super().__init__(source)
        self.message = message

    def __constructor_repr__(self):
        return "{cls}({msg}, source={src})".format(cls=self.__class__.__name__,
                                                   msg=repr(self.message),
                                                   src=repr(self.source))

    def __str__(self):
        return str(self.message)

    def __render__self__(self):
        return self.message


class NewRound(EncounterEvent):
    def __init__(self, i, source):
        super().__init__("start of round {}".format(i),
                         source)

    # TODO __render__ to make it subtitle


class TurnEvent(EncounterEvent):
    def __init__(self, current, source):
        super(TurnEvent, self).__init__(["turn of ", current.creature],
                                        source)

    def add_next(self, next_participant):
        event = EncounterEvent(["next in line is ", next_participant.creature],
                               self.source)
        self.add_sub_events(event)
        return self

    def disable(self):
        event = EncounterEvent("cannot play",
                               self.source)
        self.add_sub_events(event)
        return self


class SkipTurn(EncounterEvent):
    def __init__(self, current, source):
        super(SkipTurn, self).__init__("{} cannot play"
                                       "".format(current),
                                       source)


class EncounterStart(EncounterEvent):
    def __init__(self, source):
        super(EncounterStart, self).__init__("battle begins!", source)
    # TODO __render__ to make it a title


class EncounterEnd(EncounterEvent):
    def __init__(self, source):
        super(EncounterEnd, self).__init__("battle is over", source)
    # TODO __render__ to add some finish
