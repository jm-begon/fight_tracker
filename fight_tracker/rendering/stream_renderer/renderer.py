import os

from .util import get_stream
from ..renderer import Renderer


class StreamRenderer(Renderer):
    def __init__(self, stream=None):
        self.out = get_stream(stream)

    def flush(self, renderable):
        # renderable must be a string at this point
        print(renderable, file=self.out)

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






