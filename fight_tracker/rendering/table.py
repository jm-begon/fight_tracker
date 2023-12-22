class BoolCell(object):
    def __init__(self, value):
        self.value = value

    def __bool__(self):
        return self.value

    def __str__(self):
        return "(x)" if self.value else "( )"


class Table(object):
    def __init__(self, header=False):
        self.first_row_header = header
        self.content = [[""]]

    def new_column(self):
        self.content[-1].append("")
        return self

    def fill_cell(self, content, new_column=True):
        self.content[-1][-1] = content
        if new_column:
            self.new_column()
        return self

    def delete_cell(self):
        self.content[-1] = self.content[-1][:-1]
        return self

    def new_row(self):
        self.content.append([""])
        return self

    def fill_row(self, *args, new_row=True):
        for arg in args:
            self.fill_cell(arg, new_column=True)
        if new_row:
            self.delete_cell()
            self.new_row()
        return self

    def delete_row(self):
        self.content = self.content[:-1]
        return self

    def __str__(self):
        import os

        return os.linesep.join(
            [" ".join([cell for cell in row]) for row in self.content]
        )

    def __len__(self):
        return len(self.content)

    def __iter__(self):
        return iter(self.content)
