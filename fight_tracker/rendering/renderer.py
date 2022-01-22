from fight_tracker.creature import HpBox
from fight_tracker.events.base import Event
from fight_tracker.rendering.table import Table, BoolCell


class Renderer(object):
    def r_table(self, table):
        return str(table)

    def r_bool_cell(self, bool_cell):
        return str(bool_cell)

    def r_pv_box(self, pv_box):
        return str(pv_box)

    def r_str(self, s):
        return str(s)

    def r_event(self, event):
        return str(event)

    def dispatch(self, obj):
        if isinstance(obj, Table):
            return self.r_table(obj)
        elif isinstance(obj, BoolCell):
            return self.r_bool_cell(obj)
        elif isinstance(obj, HpBox):
            return self.r_pv_box(obj)
        elif isinstance(obj, Event):
            return self.r_event(obj)
        elif hasattr(obj, "__render__"):
            return self.dispatch(obj.__render__(self))
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


