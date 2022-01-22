import os

from .util import get_stream
from ..renderer import Renderer


class Indenter(object):
    def __init__(self, indent_width=2):
        self.width = indent_width
        self.indent = 0

    def __enter__(self):
        self.indent += self.width
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.indent -= self.width

    def __call__(self, s):
        return " "*self.indent + s


class StreamRenderer(Renderer):
    def __init__(self, stream=None, indent=2):
        self.out = get_stream(stream)
        self.indenter = Indenter(indent)

    def flush(self, renderable):
        # renderable must be a string at this point
        print(renderable, file=self.out)
        
    def r_event(self, event, indent=0):
        block = [self.indenter(str(event))]
        with self.indenter:
            for e in event:
                block.append(self.indenter(self.dispatch(e)))

        return os.linesep.join(block)

        return super(StreamRenderer, self).r_event(event)

    def r_table(self, table):
        content = []
        for row in table:
            str_row = []
            for cell in row:
                str_row.append(self.dispatch(cell))
            content.append(str_row)

        # TODO nice formatting (header, column, size, etc.)
        content_str = []
        for i, row in enumerate(content):
            if table.first_row_header and (i == 0 or i == 1):
                content_str.append("-"*80)
            content_str.append(" ".join(row))

        content_str.append("-"*80)

        return os.linesep.join(content_str)

    def r_pv_box(self, pv_box):
        return "{}/{}".format(pv_box.hp, pv_box.hp_max)






