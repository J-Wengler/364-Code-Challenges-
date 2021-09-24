from node import Node


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
        # A linked list implementation? It's a hassle, but has a lower complexity. Whatever is easiest to work on. -Alex

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

            # Create and populate adjacency list
            # Key = "AGG"
            # Value = ["GGA", "GGT"]
            adjacency_list = {}
            for read in reads:
                prefix = read[0:-1]
                suffix = read[1:]
                if prefix not in adjacency_list:
                    adjacency_list[prefix] = []  # If we don't have a node stored yet, create one!
                adjacency_list[prefix].append(suffix)  # Place the next node in the adjacency list

            # Create initial list of nodes from above adjacency list
            for seq, con in adjacency_list.items():
                new_node = Node(seq, con)
                self.nodes.append(new_node)

    def print_nodes(self):
        # Test function to make sure the nodes are being created properly
        for node in self.nodes:
            print(f"{node.get_sequence()} -> {node.get_connections()}")

    def patterns_to_adjacency_list(self):
        # I guess this will either have to write to a file or we find a way to combine it with the code above
        print("FIXME")

    def get_eularian_path(self):
        print("FIXME")

    def get_cycle(self):
        print("FIXME")

    def eularian_to_string(self):
        print("FIXME")

    def check_if_all_nodes_visited(self):
        print("FIXME")

    def get_node_from_sequence(self, node_sequence):
        temp_node = Node("NA", "NA")
        for node in self.nodes:
            if node.get_sequence == node_sequence:
                temp_node = node
        return temp_node
