from Node import Node
class Graph:

    # Path must be to adjacency list in format of
    #       AAG -> AGA,AGA
    #       AGA -> GAT
    #       ATT -> TTC
    #       CTA -> TAA
    #       etc.
    def __init__(self, in_file):
        self.in_file = in_file
        self.nodes = []
        self.e_path = [] # FIXME -> What's the best way to store this?
    

    def get_start(self, adjacency):
        return adjacency.split("->")[0]

    def get_ends(self, adjacency):
        return adjacency.split("->")[1].split(",")

    # This populates the nodes list with node objects
    # I think this needs to be reworked so that it takes in patterns and not an adjacency list 
    def make_db_graph(self):
        with open(self.in_file, "r+") as input_file:
            adjacencies = input_file.readlines()

            # Remove whitespace
            for i in range(len(adjacencies)):
                adjacencies[i] = ''.join(adjacencies[i].split())

            # Create and populate adjacency list
            # Key = "AGG"
            # Value = ["GGA", "GGT"]
            adjacency_list = {}
            for adjacency in adjacencies:
                start_node = self.get_start(adjacency)
                end_nodes = self.get_ends(adjacency)
                adjacency_list[start_node] = end_nodes

            edge_count = 0
            for connection_list in adjacency_list.values():
                edge_count += len(connection_list)

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
        





    