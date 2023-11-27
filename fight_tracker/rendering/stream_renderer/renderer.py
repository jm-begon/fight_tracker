import os
from collections import defaultdict

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
    def __init__(self, stream=None, unit=None, indent=2):
        super().__init__(unit)
        self.out = get_stream(stream)
        self.indenter = Indenter(indent)

    def flush(self, renderable):
        # renderable must be a string at this point
        print(renderable, file=self.out)

    def d_concept(self, concept):
        concept_str = super().d_concept(concept)
        if self.full_description[concept] > 0:
            return concept_str
        return f"*{concept_str}*"
        
    def r_tree(self, tree, indent=0):
        block = [self.indenter(self.dispatch(tree.content))]
        with self.indenter:
            for e in tree:
                block.append(self.indenter(self.dispatch(e)))

        return os.linesep.join(block)

    def r_table(self, table):
        content = []
        col_len = defaultdict(int)
        for i, row in enumerate(table):
            str_row = []
            for j, cell in enumerate(row):
                content_str = self.dispatch(cell)
                str_row.append(content_str)
                col_len[j] = max(col_len[j], len(content_str))
            content.append(str_row)

        content_str = []
        sep = " | "
        headline = "+-" + "-+-".join(["-"*col_len[l] for l in range(len(col_len))]) + "-+"

        content_str.append("/" + headline[1:])
        for i, row in enumerate(content):
            tmp = []
            for j, col_content in enumerate(row):
                s = col_content.ljust(col_len[j])
                tmp.append(s)
            content_str.append("| " + sep.join(tmp) + " |")
            if table.first_row_header and i == 0:
                content_str.append(headline)

        content_str.append(headline[:-1] + "/")

        return os.linesep.join(content_str)

    def r_hp_bar(self, pv_box):
        percents = pv_box.hp / pv_box.hp_max * 100
        return "{}/{} ({:.1f} %)".format(pv_box.hp, pv_box.hp_max, percents)






