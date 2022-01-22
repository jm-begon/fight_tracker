from fight_tracker.util import ObserverMixin


class Logger(ObserverMixin):
    def log(self, event):
        pass

    def update(self, event):
        self.log(event)


class HistoryDecorator(Logger):
    def __init__(self, decorated):
        self.decorated = decorated
        self.history = []

    def log(self, event):
        self.history.append(event)
        self.decorated.log(event)
