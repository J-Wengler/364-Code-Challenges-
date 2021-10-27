from node import Node
from tree import Tree


def get_node(string_node, node_dict):
    assert(isinstance(string_node, str))
    if string_node in node_dict:
        return node_dict[string_node]

    new_node = Node()
    new_node.label = string_node
    node_dict[string_node] = new_node
    return new_node


def build_simple_tree(input_file_path):
    nodes = {}
    with open(input_file_path, 'r+') as input_file:
        swap_edge = input_file.readline().split()
        for line in input_file.readlines():
            string_nodes = line.rstrip().split("->")

            left = get_node(string_nodes[0], nodes)
            right = get_node(string_nodes[1], nodes)

            left.add_link(right)  # The input should give us the other direction separately

    # root = make_root(nodes, left, right)
    return swap_edge, Tree(nodes)

