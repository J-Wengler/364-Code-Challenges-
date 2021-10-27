class Tree:
    def __init__(self, nodes, root=None):
        self.nodes = nodes
        self.root = root
        # leaf = self.get_leaf()
        # self.sequence_length = len(leaf.label)

    def __repr__(self):
        r_string = ''
        for node in self.nodes:
            r_string += node.__repr__() + '\n'
        return r_string

    def get_ripe_node(self):
        for node in self.nodes.values():
            if node.is_ripe():
                return node

        # If no ripe nodes:
        return None

    # Returns total edge weight values in the tree. This represents the total number of substitutions.
    def get_parsimony_score(self):
        score = 0
        for node in self.nodes.values():
            score += node.distance_to_parent
        return score

    # Returns a list of each edge in tuple form. No duplicates to account.
    # Format is (first, second, weight)
    # Example return is list of: (ATCCC, GGCCC, 2)
    def get_edges(self):
        adjacencies = []
        for node in self.nodes.values():
            if node.parent is not None:
                adjacencies.append((node.label, node.parent.label, node.distance_to_parent))
        return adjacencies

    def get_leaf(self):
        current_node = self.root
        while len(current_node.children) > 0:
            current_node = current_node.children[0]
        return current_node  # The leftmost leaf in the tree
