class Node:
    def __init__(self, num):
        self.children = [] # List of Nodes
        self.parent = None # Node
        self.num = num # number node name
        self.label = "" # i.e. agctca
        self.sk = dict.fromkeys(['A', 'C', 'G', 'T']) # indexes are acgt
        self.tag = None
        self.distance_to_parent = 0  # The substitutions required to turn child to parent i.e. AGG->TGG=1

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
            + 'children:' + children_nums.__repr__() + '\n' \
            + 'parent:' + str(parent_num) + '\n' \
            + 'dist to self:' + str(self.distance_to_parent) + '\n' \
            + 'sk:' + self.sk.__repr__() + '\n' \
            + 'tag:' + str(tag) + '\n'

    def is_ripe(self):
        if self.tag == 1:
            return False
        for child in self.children:
            if child.tag == 0:
                return False
        # If tag is 0 and both children's tags are 1
        return True

    def is_leaf(self):
        return len(self.children) is 0

    def remove_child(self, child):
        child_index = -1
        child_itr = 0
        for node in self.children:
            if node.num == child:
                child_index =  child_itr
            child_itr = child_itr + 1
        self.children.pop(child_index)
