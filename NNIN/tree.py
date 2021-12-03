class Tree:
    def __init__(self, T, root = None):
        self.T = T
        self.root = root
        self.sp = -1

    def __repr__(self):
        r_string = ''
        for node in self.T.keys():
            r_string = r_string + self.T[node].__repr__()
        return r_string

    def get_ripe_node(self):
        for node in self.T.values():
            if node.is_ripe():
                return node

        # If no ripe nodes:
        return None

    # Returns total edge weight values in the tree. This represents the total number of substitutions.
    def get_parsimony_score(self):
        score = 0
        for node in self.T.values():
            score += node.distance_to_parent
        return score

    def reset_tree(self):
        for node in self.T.values():
            node.full_reset()
        self.reset_leaves




    def reset_family(self):
        for node in self.T.values():
            node.reset_relationships()
        self.reset_leaves()

    def reset_leaves(self):
        for node in self.T.values():
            if len(node.links) > 1:
                node.is_leaf = False
            else:
                node.is_leaf = True

    # Returns a list of each edge in tuple form. No duplicates to account.
    # Format is (first, second, weight)
    # Example return is list of: (ATCCC, GGCCC, 2)

    def get_num_links(self):
        total_links = 0
        for node in self.T.values():
            total_links += len(node.links)
        #print(f"TOTAL LINKS : {total_links}")
        return(total_links)


    def get_edges(self):
        adjacencies = []
        for node in self.T.values():
            if node.parent is not None:
                adjacencies.append((node.label, node.parent.label, node.distance_to_parent))
            #adjacencies.append((node.label, node.parent.label, node.distance_to_parent))
        return adjacencies
