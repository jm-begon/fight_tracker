from .base import TargetedEvent


class Conditioned(TargetedEvent):
    def __init__(self, target, condition, source):
        super().__init__(target, source)
        self.condition = condition

    def __constructor_repr__(self):
        return "{}({}, {}, {})".format(self.__class__.__name__,
                                       repr(self.target),
                                       repr(self.condition),
                                       repr(self.source))

    def __render_self_event__(self):
        return ["is", self.condition]
