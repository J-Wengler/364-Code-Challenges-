from node import Node
import random


class Graph:

    # Path must be to adjacency list in format of
    #       AAG -> AGA,AGA
    #       AGA -> GAT
    #       ATT -> TTC
    #       CTA -> TAA
    #       etc.
    def __init__(self, in_file):
        self.in_file = in_file
        self.k = 0  # This is the k in k-mer. Might make some code easier to read. Use it if you need.
        self.nodes = []
        self.e_path = []  # FIXME -> What's the best way to store this?
        self.edges = 0
        self.first = None
        self.last = None

    # This populates the nodes list with node objects
    def make_db_graph(self):
        # In file format:
        # <k>
        # <lines of reads of k length>
        with open(self.in_file, "r+") as input_file:
            self.k = int(input_file.readline())
            reads = []

            # Remove whitespace, ignore empty lines
            for line in input_file.readlines():
                line = ''.join(line.split())
                if line != '':
                    assert len(line) == self.k
                    reads.append(line)

            # Create and populate node list
            # Connect nodes

            # I changed this code so that rather than creating an adjacency list, it just automatically creates the
            # nodes and connects them, making a linked list of nodes. That way we don't have to cycle back through the
            # adjacency list - Connor
            for read in reads:
                prefix = read[0:-1]
                suffix = read[1:]

                this_node = None
                next_node = None

                # if nodes exist for prefix or suffix, assign them
                for node in self.nodes:
                    if node.get_sequence() == prefix:
                        this_node = node
                    if node.get_sequence() == suffix:
                        next_node = node

                # if nodes don't exist yet for prefix of suffix, create them
                if this_node is None:
                    this_node = Node(prefix)
                    self.nodes.append(this_node)

                if next_node is None:
                    next_node = Node(suffix)
                    self.nodes.append(next_node)

                # connect the prefix node to the suffix node (and add one to the in degree of the suffix)
                this_node.add_connection(next_node)
                next_node.increment_in_degree()
                self.edges += 1

    def get_eulerian_path(self):
        # Find first and last node, first node has more out than in, last node has more in than out
        for node in self.nodes:
            if node.get_in_degree() < node.get_out_degree():
                self.first = node
            elif node.get_in_degree() > node.get_out_degree():
                self.last = node

        # add a connection between last and first to make it an Eulerian cycle
        self.last.add_connection(self.first)
        self.first.increment_in_degree()
        self.edges += 1

        # Get initial cycle
        cycle = self.get_cycle()

        # if some edges are not traversed, loop through it again
        new_cycle = []
        while self.edges > 0:

            # find the next place to start (node with unvisited edges), get it's index and use that to "traverse"
            # the original cycle starting and ending at that node
            new_start = self.get_new_start(cycle)
            new_start_index = cycle.index(new_start)
            new_cycle.extend(cycle[new_start_index:])
            new_cycle.extend(cycle[:new_start_index])

            # visit new edges from new start node, add them to the cycle
            new_cycle.extend(self.get_new_cycle(new_start))
            cycle = new_cycle
            new_cycle = []

        # the cycle may not be correctly ordered at this point, since it didn't necessarily start at the first node
        # this orders the cycle by finding the index of the first node (assigning at beginning of this function)
        # and then making that the starting index
        first_index = cycle.index(self.first)
        ordered_cycle = []
        ordered_cycle.extend(cycle[first_index:])
        ordered_cycle.extend(cycle[:first_index])
        self.e_path = ordered_cycle

    # Find a node that has unvisited edges
    def get_new_start(self, cycle) -> Node:
        for node in cycle:
            if node.get_num_unvisited_edges() > 0:
                return node

    # Get the initial cycle, starting at a random node and then walking through until you get stuck
    def get_cycle(self):
        cycle = []
        current = random.choice(self.nodes)
        while self.edges > 0 and current.get_num_unvisited_edges() > 0:
            cycle.append(current)
            next_node = current.get_next()
            current.visit_edge(next_node)
            current = next_node
            self.edges -= 1

        return cycle

    # Get a new cycle (to add to the previous cycle), starting at a specified node with unvisited edges
    def get_new_cycle(self, new_start):
        cycle = []
        current = new_start
        while self.edges > 0 and current.get_num_unvisited_edges() > 0:
            cycle.append(current)
            next_node = current.get_next()
            current.visit_edge(next_node)
            current = next_node
            self.edges -= 1

        return cycle

    # Write to string, for the first node use all nucleotides, afterwards just adding on the last one
    def eulerian_to_string(self):
        sequence = ""
        for node in self.e_path:
            if node == self.first:
                sequence += node.get_sequence()
            else:
                sequence += node.get_sequence()[-1]
        print(sequence)

    def print_nodes(self):
        # Test function to make sure the nodes are being created properly
        for node in self.nodes:
            print(f"{node.get_sequence()} -> {node.get_connections()}")