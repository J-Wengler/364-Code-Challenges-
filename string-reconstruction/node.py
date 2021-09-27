import random


class Node:

    # Constructor
    # sequence -> String representation of node AKA "ATCGT"
    def __init__(self, sequence):
        self.sequence = sequence
        self.connections = []
        self.num_edges = 0
        self.num_times_to_visit = 0
        self.out_degree = 0
        self.in_degree = 0

    # add a connecting node, increase out_degree and num_edges
    def add_connection(self, node):
        self.connections.append(node)
        self.out_degree += 1
        self.num_edges += 1

    def increment_in_degree(self):
        self.in_degree += 1

    def get_connections(self):
        return self.connections

    def get_sequence(self):
        return self.sequence

    def get_in_degree(self):
        return self.in_degree

    def get_out_degree(self):
        return self.out_degree

    def get_num_unvisited_edges(self):
        return len(self.connections)

    # when an edge is visited, this removes the node from the list
    def visit_edge(self, node):
        self.connections.remove(node)

    def get_next(self):
        return random.choice(self.connections)
