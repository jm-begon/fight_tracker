from .events.logger import Logger


class Narrator(Logger):
    def __init__(self):
        self.history = []

    def hello(self):
        pass

    def update(self, event):
        self.history.append(event)


class ConsoleNarrator(Narrator):
    # TODO channel in init (default stderr?) + self.print
    def hello(self):
        print("Hello! I will be the narrator for this encounter.")

    def update(self, event):
        super().update(event)
        print(str(event))
