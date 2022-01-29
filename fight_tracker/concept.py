class Concept:
    def short_repr(self):
        return self.__class__.__name__

    def mid_repr(self):
        return self.short_repr()

    def long_repr(self):
        return self.short_repr()
