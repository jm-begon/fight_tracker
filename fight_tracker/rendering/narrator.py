from fight_tracker.events.logger import Logger


class Narrator(Logger):
    def __init__(self, renderer):
        self.history = []
        self.renderer = renderer

    def hello(self):
        self.renderer("Hello! I will be the narrator for this encounter.")

    def log(self, event):
        super(Narrator, self).log(event)
        self.renderer(event)
        # TODO clock rounds by encounters
        self.history.append(event)
