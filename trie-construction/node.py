from edge import Edge

class Node:
    def __init__(self, num):
        self.n = num
        self.out_edges = []

    def __repr__(self):
        out_str = f" NUM : {self.n}\n"
        for edge in self.out_edges:
            edge_str = f"CONNECTION TO {edge.to.n} WITH LABEL {edge.label}\n"
            out_str += edge_str
        return out_str

    def check_edge(self, char):
        for edge in self.out_edges:
            if edge.label == char:
                return edge.to

        return False

