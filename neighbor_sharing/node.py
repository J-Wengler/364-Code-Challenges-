class Node:
    def __init__(self):
        self.children = []  # List of Nodes
        self.parent = None  # Node
        self.label = ""  # i.e. agctca
        self.sk = dict.fromkeys(['A', 'C', 'G', 'T'])  # indexes are acgt
        self.is_sk_processed = False
        self.distance_to_parent = 0  # The substitutions required to turn child to parent i.e. AGG->TGG=1
        self.is_leaf = False
        self.links = []  # lists of nodes that are connected to this one. Used in construction.

    def __repr__(self):
        children_labs = [child.label for child in self.children]
        return \
            'Label:' + self.label \
            + 'children:' + children_labs.__repr__() + '\n' \
            + 'dist to self:' + str(self.distance_to_parent) + '\n' \
            + 'sk:' + self.sk.__repr__() + '\n' \
            + 'is sk processed:' + str(self.is_sk_processed) + '\n'

# Returns whether this node is ready to be sk processed
    def is_ripe(self):
        if self.is_sk_processed:
            return False
        for child in self.children:
            if not child.is_sk_processed:
                return False
        return True

    def add_link(self, linked_node):
        self.links.append(linked_node)
