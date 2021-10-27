from node import Node
from tree import Tree


def get_node(string_node, node_dict):
    assert(isinstance(string_node, str))
    if string_node in node_dict:
        return node_dict[string_node]

    new_node = Node()
    if not string_node[0].isnumeric():
        new_node.label = string_node
        new_node.is_leaf = True

    node_dict[string_node] = new_node
    return new_node


def point_to_root(parent_node):
    for child in parent_node.links:
        parent_node.children.append(child)
        child.parent = parent_node
        child.links.remove(parent_node)
        point_to_root(child)


def make_root(node_dict, node1, node2):
    root = Node()
    node_dict["root"] = root

    node1.links.remove(node2)
    node2.links.remove(node1)

    root.children.append(node1)
    root.children.append(node2)

    node1.parent = root
    node2.parent = root

    point_to_root(node1)
    point_to_root(node2)

    return root


def buildtreefromfile(file_name):
    nodes = {}
    with open(file_name, 'r+') as input_file:
        n = int(input_file.readline())
        for line in input_file.readlines():
            string_nodes = line.rstrip().split("->")

            left = get_node(string_nodes[0], nodes)
            right = get_node(string_nodes[1], nodes)

            left.add_link(right)  # The input should give us the other direction separately

    root = make_root(nodes, left, right)
    return Tree(nodes, root)
