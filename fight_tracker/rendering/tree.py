class Tree:
    def __init__(self, content):
        self.content = content
        self.children = []

    def add_child(self, tree):
        self.children.append(tree)

    def __iter__(self):
        return iter(self.children)