# TODO: - State for Events
#       - Events are not callable
#       - Delayed Events are lazy
from ..rendering.tree import Tree


class Event(object):
    def __init__(self, source):
        self._source = source
        self._sub_events = []  # consequences

    def notify(self):
        self.source.notify(self)
        return self

    @property
    def source(self):
        return self._source

    def add_sub_events(self, event):
        self._sub_events.append(event)
        return self

    def __iter__(self):
        return iter(self._sub_events)

    def __constructor_repr__(self):
        return "{cls}({source})".format(
            cls=self.__class__.__name__, source=repr(self.source)
        )

    def __repr__(self):
        s = self.__constructor_repr__()
        for sub_event in self._sub_events:
            s = s + ".add_sub_events({})".format(repr(sub_event))
        return s

    def __str__(self):
        return repr(self)

    def __render__self__(self):
        return str(self)

    def __render__(self):
        root = Tree(self.__render__self__())
        for event in self:
            root.add_child(event.__render__())
        return root


class TargetedEvent(Event):
    def __init__(self, target, source):
        super(TargetedEvent, self).__init__(source)
        self.target = target
        self.source_creature = None

    def add_source_creature(self, creature):
        self.source_creature = creature
        return self

    def __constructor_repr__(self):
        s = "{cls}(target={target}, source={source})" "".format(
            cls=self.__class__.__name__,
            target=repr(self.target),
            source=repr(self.source),
        )
        if self.source_creature is not None:
            s = s + ".add_source_creature({})".format(repr(self.source_creature))
        return s

    def add_source_str(self, s):
        if self.source_creature is None:
            return s
        return "{} from {}".format(s, self.source.name)

    def __str__(self):
        return self.add_source_str(
            "{} receives {}" "".format(self.target.name, self.__class__.__name__)
        )

    def __render__self__(self):
        ls = [self.target]
        ls.extend(self.__render_self_event__())
        if self.source_creature is not None:
            ls.append("from")
            ls.append(self.source)
        return ls

    def __render_self_event__(self):
        return [f"receives {self.__class__.__name__}"]


class MessageEvent(TargetedEvent):
    def __init__(self, target, message, source):
        super().__init__(target, source)
        self.message = message

    def __constructor_repr__(self):
        return "{}({}, {}, {})".format(
            self.__class__.__name__,
            repr(self.target),
            repr(self.message),
            repr(self.source),
        )

    def __render_self_event__(self):
        if isinstance(self.message, str):
            return [self.message]
        return self.message


class Attacked(TargetedEvent):
    pass


class Hit(TargetedEvent):
    pass


class Missed(TargetedEvent):
    pass


class Damaged(TargetedEvent):
    def __init__(self, target, damage, source):
        super().__init__(target, source)
        if isinstance(damage, int):
            damage = Damage(damage)
        self.damage = damage

    def __str__(self):
        return self.add_source_str("{} takes {}".format(self.target.name, self.damage))

    def __int__(self):
        return int(self.damage)

    def __render_self_event__(self):
        return ["takes", self.damage]


class Healed(TargetedEvent):
    def __init__(self, target, bonus, source):
        super().__init__(target, source)
        self.bonus = bonus

    def __str__(self):
        return self.add_source_str(
            "{} regains {} hit point(s)" "".format(self.target.name, int(self.bonus))
        )

    def __int__(self):
        return int(self.bonus)

    def __render_self_event__(self):
        return [f"regains {int(self.bonus)} hit point(s)"]


class HPEvent(MessageEvent):
    pass


class EncounterEvent(Event):
    def __init__(self, message, source):
        super().__init__(source)
        self.message = message

    def __constructor_repr__(self):
        return "{cls}({msg}, source={src})".format(
            cls=self.__class__.__name__, msg=repr(self.message), src=repr(self.source)
        )

    def __str__(self):
        return str(self.message)

    def __render__self__(self):
        return self.message


class NewRound(EncounterEvent):
    def __init__(self, i, source):
        super().__init__("start of round {}".format(i), source)

    # TODO __render__ to make it subtitle


class TurnEvent(EncounterEvent):
    def __init__(self, current, source):
        super(TurnEvent, self).__init__(["turn of ", current.creature], source)

    def add_next(self, next_participant):
        event = EncounterEvent(
            ["next in line is ", next_participant.creature], self.source
        )
        self.add_sub_events(event)
        return self

    def disable(self):
        event = EncounterEvent("cannot play", self.source)
        self.add_sub_events(event)
        return self


class SkipTurn(EncounterEvent):
    def __init__(self, current, source):
        super(SkipTurn, self).__init__("{} cannot play" "".format(current), source)


class EncounterStart(EncounterEvent):
    def __init__(self, source):
        super(EncounterStart, self).__init__("battle begins!", source)

    # TODO __render__ to make it a title


class EncounterEnd(EncounterEvent):
    def __init__(self, source):
        super(EncounterEnd, self).__init__("battle is over", source)

    # TODO __render__ to add some finish


class Conditioned(TargetedEvent):
    def __init__(self, target, condition, source):
        super().__init__(target, source)
        self.condition = condition

    def __constructor_repr__(self):
        return "{}({}, {}, {})".format(
            self.__class__.__name__,
            repr(self.target),
            repr(self.condition),
            repr(self.source),
        )

    def __render_self_event__(self):
        return ["is", self.condition]
