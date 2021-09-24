class Node:

    # Constructor
    # sequence -> String representation of node AKA "ATCGT"
    # connections -> list of Strings representing the connections that exist AKA ["TCGAA", "CGAAT", "TAGAGG"]
    def __init__(self, sequence, connections):
        self.sequence = sequence
        self.connections = connections 
        self.been_visited = False

    def been_visited(self):  # TODO: Switch to meaning every node has been visited. -Alex
        return self.been_visited

    def get_connections(self):
        return self.connections

    def get_sequence(self):
        return self.sequence
