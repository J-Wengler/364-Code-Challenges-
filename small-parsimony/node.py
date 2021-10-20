class Node:
    def __init__(self, num):
        self.children = [] # List of Nodes
        self.parent = None # Node
        self.num = num # number node name
        self.label = None # i.e. agctca
        self.sk = dict.fromkeys(['A', 'C', 'G', 'T']) # indexes are acgt
        self.tag = None

    def __repr__(self):
        label = ''
        parent_num = ''
        tag = ''
        if self.label:
            label = self.label
        if self.parent:
            parent_num = self.parent.num
        if self.tag is not None:
            tag = self.tag
        children_nums = [child.num for child in self.children]
        return str(self.num) + ':' + label + '\n' \
            + 'chilren:' + children_nums.__repr__() + '\n' \
                + 'parent:' + str(parent_num) + '\n' \
                    + 'k:' + self.sk.__repr__() + '\n' \
                        + 'tag:' + str(tag) + '\n'