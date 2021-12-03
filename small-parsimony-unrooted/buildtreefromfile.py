from node import Node
from tree import Tree

# Recursively parse from root down, adding each layer as children to the previous layer
def parse_from_root(parent_node):
    for child in parent_node.links:
        parent_node.children.append(child)
        child.parent = parent_node
        child.links.remove(parent_node)
        parse_from_root(child)

# Take two nodes and insert a root between them
# Then parse the new relationships from that node
def make_root(T, left, right):
    root = Node()
    T["root"] = root

    left.links.remove(right)
    right.links.remove(left)

    root.children.append(left)
    root.children.append(right)

    left.parent = root
    right.parent = root

    parse_from_root(left)
    parse_from_root(right)

    return root

# Either make a new node from a given string/number or return the appropiate existing node
def get_node(string_node, T):
    if string_node in T:
        return T[string_node]

    new_node = Node()

    # If the label is given then set it and declare the node a leaf
    if not string_node[0].isnumeric():
        new_node.label = string_node
        new_node.is_leaf = True
    T[string_node] = new_node
    return new_node

# Parse through the data and create a unrooted tree, then root and parse it
def build_simple_tree(input_file_path):
    T = {}
    with open(input_file_path, 'r+') as input_file:
        n = input_file.readline()
        for line in input_file.readlines():
            line = line.rstrip().split("->")
            left = get_node(line[0], T)
            right = get_node(line[1], T)

            left.links.append(right)
    # Use last two adjacent nodes to insert root
    root = make_root(T, left, right)
    return Tree(T, root)    