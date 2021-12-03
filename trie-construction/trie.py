from node import Node
from edge import Edge

class Trie:
    def __init__(self):
        self.nodes = []
        self.root = None

    def __repr__(self):
        out_str = ""
        for node in self.nodes:
            for edge in node.out_edges:
                edge_str = f"{edge.origin.n} {edge.to.n} {edge.label}\n"
                out_str += edge_str
        return out_str
    
    def add_root(self):
        root = Node(0)
        self.root = root
        self.nodes.append(root)

    def add_node(self, char, cur_node):
        new_node = Node(len(self.nodes))
        new_edge = Edge(cur_node, new_node, char)
        cur_node.out_edges.append(new_edge)
        self.nodes.append(new_node)
        return new_node

        #FIXME -> ADD a new node, and an edge connecting the two, return the new node


    def add_pattern(self, pattern):
        cur_node = self.root 
        for char in pattern:
            if cur_node.check_edge(char) is not False:
                cur_node = cur_node.check_edge(char)
            else:
                cur_node = self.add_node(char, cur_node)



