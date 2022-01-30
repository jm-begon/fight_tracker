class Tree:
    def __init__(self, content):
        self.content = content
        self.children = []

    def add_child(self, tree):
        if not isinstance(tree, Tree):
            tree = self.__class__(tree)
        self.children.append(tree)
        return self

    def add_children(self, *trees):
        for tree in trees:
            self.add_child(tree)
        return self

    def __iter__(self):
        return iter(self.children)
