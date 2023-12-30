import os
from collections import defaultdict
from typing import Collection, List

from ..card import Card, CardSeparator, Description
from ..renderer import Renderer
from .util import get_stream


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
        return " " * self.indent + s


class StreamRenderer(Renderer):
    DEFAULT_CARD_MAX_LENGTH = 80

    def __init__(self, stream=None, unit=None, indent=2):
        super().__init__(unit)
        self.out = get_stream(stream)
        self.indenter = Indenter(indent)
        self.card_max_length = self.DEFAULT_CARD_MAX_LENGTH

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
        headline = (
            "+-" + "-+-".join(["-" * col_len[l] for l in range(len(col_len))]) + "-+"
        )

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
        hp = int(pv_box.hp)
        hp_max = int(pv_box.hp_max)
        percents = 100 * int(pv_box.hp) / int(pv_box.hp_max)
        return f"{hp}/{hp_max} ({percents:.1f} %)"

    def r_description(self, description: Description) -> str:
        tmp = []
        if description.name is not None:
            tmp.append(self.dispatch(description.name))

        for key, value in description:
            dispatched_value = self.dispatch(value)
            tmp.append(f"- \033[1m{key}\033[0m: {dispatched_value}")

        return os.linesep.join(tmp)

    def r_card(self, card: Card) -> str:
        tmp = [card.title.upper()]
        for x in card:
            if isinstance(x, CardSeparator):
                x_ = "-" * (self.card_max_length - 4)
                if x.name:
                    x_ += x.name
                x = x_[-(self.card_max_length - 4) :]
            tmp.extend(self.dispatch(x).split(os.linesep))

        trimed_tmp: List[str] = []
        for x in tmp:
            trimed_tmp.extend(self.split_at_length(x, self.card_max_length - 4))

        final = ["/" + "-" * (self.card_max_length - 2) + "+"]
        for x in trimed_tmp:
            final.append(f"| {self.ljust(x, self.card_max_length - 4)} |")

        final.append("+" + "-" * (self.card_max_length - 2) + "/")

        return os.linesep.join(final)

    def ljust(self, s: str, width: int, fillchar: str = " ") -> str:
        l1 = len(s)
        l2 = len(self.strip_formating(s))
        dl = l1 - l2
        if dl <= 0:
            dl = 0
        return s.ljust(width + dl, fillchar)

    def split_at_length(self, s: str, max_length: int) -> List[str]:
        if len(s) <= max_length:
            return [s.strip()]

        cutoff = max_length
        while cutoff > 0 and not s[cutoff].isspace():
            cutoff -= 1

        if cutoff == 0:
            # Failed to cut
            cutoff = max_length

        return [s[:cutoff].strip()] + self.split_at_length(
            s[cutoff:].strip(), max_length
        )

    def strip_formating(self, s: str) -> str:
        return s.replace("\x1B[1m", "").replace("\x1B[3m", "").replace("\x1B[0m", "")
