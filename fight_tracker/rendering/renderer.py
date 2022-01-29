from .table import Table, BoolCell
from .tree import Tree



class Renderer(object):
    def d_concept(self, concept):
        return self.dispatch(concept.short_repr())

    def r_table(self, table):
        return str(table)

    def r_bool_cell(self, bool_cell):
        return str(bool_cell)

    def r_pv_box(self, pv_box):
        return str(pv_box)

    def r_str(self, s):
        return str(s)

    def r_tree(self, tree):
        ls = [self.dispatch(e) for e in tree]
        return self.concat([self.dispatch(tree.content),
                            self.concat(ls)])

    def concat(self, iterable):
        return " ".join(iterable)

    def dispatch(self, obj):
        from ..concept import Concept
        from ..creature import HpBox

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
        elif isinstance(obj, HpBox):
            return self.r_pv_box(obj)
        elif isinstance(obj, Tree):
            return self.r_tree(obj)
        else:
            return self.r_str(obj)

    def flush(self, renderable):
        pass

    def __call__(self, obj):
        renderable = self.dispatch(obj)
        self.flush(renderable)
        return self

    def __lshift__(self, other):
        self(other)


