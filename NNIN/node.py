class Node:
    def __init__(self):
        self.children = [] # List of Nodes
        self.parent = None # Node
        self.swap_children = []
        #self.num = num # number node name
        self.label = "" # i.e. agctca
        self.sk = dict.fromkeys(['A', 'C', 'G', 'T']) # indexes are acgt
        self.tag = None
        self.links = []
        self.is_leaf = False
        self.distance_to_parent = 0
        self.parse_links_copy = []  # The substitutions required to turn child to parent i.e. AGG->TGG=1

    def __repr__(self):

        parent_str = "None"
        if self.parent is not None:
            parent_str = f"{self.parent.label} "
        child_str = "None"
        if len(self.children) > 0:
            child_str = ""
            for child in self.children:
                child_str += f"{child.label} "
        link_str = "None"
        if len(self.links) > 0:
            link_str = ""
            for link in self.links:
                if link.label == "":
                    link_str += "INTERNAL-NODE "
                else:
                    link_str += f"{link.label} "
            
        out_str = f"\nNODE LABEL : {self.label}\nNODE PARENT LABEL : {parent_str}\nCHILDREN LABELS : {child_str}\nLEAF? : {self.is_leaf}\nLINK LABELS : {link_str}\n"
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
        return self.is_leaf

    def full_reset(self):
        if self.parent is not None:
            if self.parent not in self.links:
                self.links.append(self.parent)
        for child in self.children:
            if child not in self.links:
                self.links.append(child)
        
        self.parent = None
        self.children = []
        self.distance_to_parent = 0
        self.sk = dict.fromkeys(['A', 'C', 'G', 'T'])
        if not self.is_leaf:
            self.label = ""

    def remove_child(self, child):
        child_index = -1
        child_itr = 0
        for node in self.children:
            if node.num == child:
                child_index =  child_itr
            child_itr = child_itr + 1
        self.children.pop(child_index)

    def reset_relationships(self):
        if self.parent is not None:
            if self.parent not in self.links:
                self.links.append(self.parent)
        for child in self.children:
            if child not in self.links:
                self.links.append(child)
        self.parent = None
        self.children = []
        self.distance_to_parent = 0
        if not self.is_leaf:
            self.label = ""
