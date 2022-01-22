# TODO: - State for Events
#       - Events are not callable
#       - Delayed Events are lazy


class Event(object):
    def __repr__(self):
        return "{cls}()".format(cls=self.__class__.__name__)

    def __str__(self):
        return repr(self)


class MessageEvent(Event):
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return "{cls}({msg})".format(cls=self.__class__.__name__,
                                     msg=repr(self.message))

    def __str__(self):
        return str(self.message)


# class DelayedEvent(Event):
#     def __init__(self, event):
#         self.decorated = event
#
#     def __call__(self, *args, **kwargs):
#         pass
#
#
# class Trigger(object):
#     def __rshift__(self, other):
#         # quick and dirty
#         if isinstance(other, Event):
#             other()
#         return other





class CallbackEvent(MessageEvent):
    def __init__(self, callback, message):
        super(CallbackEvent, self).__init__(message)
        self.message = message
        self.callback = callback

    def __call__(self, *args, **kwargs):
        return self.callback()


class TargetedEvent(Event):
    def __init__(self, target, source=None):
        self.target = target
        self.source = source

    def __repr__(self):
        return "{cls}(target={target}, source={source})" \
               "".format(cls=self.__class__.__name__,
                         target=repr(self.target),
                         source=repr(self.source))

    def add_source(self, s):
        if self.source is None:
            return s
        return "{} from {}".format(s, self.source.name)

    def __str__(self):
        return self.add_source("{} receives {}"
                               "".format(self.target.name, self.__class__.__name__))