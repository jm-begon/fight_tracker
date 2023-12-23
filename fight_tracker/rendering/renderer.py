from collections import defaultdict

from ..concept import Concept
from ..mechanics.speed import Speed, Unit
from .misc import HPBar
from .table import BoolCell, Table
from .tree import Tree


class Renderer(object):
    def __init__(self, unit=None):
        self.full_description = defaultdict(int)
        self.unit = unit if unit is not None else Unit.SQUARES

    def d_concept(self, concept):
        if self.full_description[concept] > 0:
            return self.dispatch(concept.long_repr())
        return self.dispatch(concept.short_repr())

    def r_table(self, table):
        return str(table)

    def r_bool_cell(self, bool_cell):
        return str(bool_cell)

    def r_hp_bar(self, hp_bar):
        return str(hp_bar)

    def r_str(self, s):
        return str(s)

    def r_tree(self, tree):
        ls = [self.dispatch(e) for e in tree]
        return self.concat([self.dispatch(tree.content), self.concat(ls)])

    def r_speed(self, speed):
        unit = speed.unit
        try:
            speed.unit = self.unit
            s = str(speed)
        finally:
            speed.unit = unit
        return s

    def concat(self, iterable):
        return " ".join(iterable)

    def dispatch(self, obj):
        if hasattr(obj, "__render__"):
            return self.dispatch(obj.__render__())
        elif isinstance(obj, list) or isinstance(obj, tuple):
            # iterable would be too generic
            return self.concat([self.dispatch(obj_i) for obj_i in obj])
        elif isinstance(obj, Concept):
            return self.d_concept(obj)
        elif isinstance(obj, Table):
            return self.r_table(obj)
        elif isinstance(obj, BoolCell):
            return self.r_bool_cell(obj)
        elif isinstance(obj, HPBar):
            return self.r_hp_bar(obj)
        elif isinstance(obj, Tree):
            return self.r_tree(obj)
        elif isinstance(obj, Speed):
            return self.r_speed(obj)
        else:
            return self.r_str(obj)

    def flush(self, renderable):
        pass

    def __call__(self, obj):
        renderable = self.dispatch(obj)
        self.flush(renderable)
        return self

    def __lshift__(self, other):
        # TODO move to game ?
        # Reentrant
        self.full_description[other] += 1
        try:
            self(other)
        finally:
            self.full_description[other] -= 1
