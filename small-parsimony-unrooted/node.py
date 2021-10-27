class Node:
    def __init__(self, num):
        self.children = [] # List of Nodes
        self.parent = None # Node
        self.num = num # number node name
        self.label = num # i.e. agctca
        self.sk = dict.fromkeys(['A', 'C', 'G', 'T']) # indexes are acgt
        self.tag = None
        self.links = []
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
        children_nums = [child.num for child in self.links]
        child_str = ""
        if len(self.children) == 0:
            child_str = "Empty"
        else:
            for child in self.children:
                child_str += f"{child.num} "
        parent_str = ""
        if self.parent == None:
            parent_str = "None"
        else:
            parent_str = f"{self.parent.num}"
        link_str = ""
        for link in self.links:
            link_str += f"{link.num} "
        out_str = f"NUM : {self.num} \nLABEL : {self.label} \nPARENT : {parent_str} \nCHILDLEN : {child_str}\nLINKS : {link_str}\n"
        return out_str
        

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
