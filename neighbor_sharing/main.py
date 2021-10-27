from buildtreefromfile import buildtreefromfile
from BuildSimpleTree import build_simple_tree


# Gets the best, lowest-parsimony score possible for a given parent (ripe_node)
# at a given nucleotide (k).
def get_min_score(ripe_node, k, character):
    left = ripe_node.children[0]
    right = ripe_node.children[1]

    min_key_left, min_value_left = get_min_key_value(left, k, character)
    min_key_right, min_value_right = get_min_key_value(right, k, character)

    return min_value_left + min_value_right


# Returns the best letter and the value that allows you to get to parent k
# Order of keys in character is tiebreaker
#
# Example:
# node.sk = {A:1, C:2, G:2, T:1}
# k = 'T'
# return -> min_key = 'T', min_value = 1
def get_min_key_value(node, k, character):
    min_value = float('inf')
    min_key = 'x'  # Only returned if no value in sk is less than inf
    for key in character:
        val = node.sk[key]
        if key != k:
            val += 1
        if val < min_value:
            min_value = val
            min_key = key
    return min_key, min_value


# Recursively updates the label for nodes by appending the best guess stored in the sk values
# Also increases the distances accordingly
def update_labels(root, character):
    assert(not root.is_leaf)

    min_k = 'z'
    min_value = float('inf')
    for k in character:
        if root.sk[k] < min_value:
            min_value = root.sk[k]
            min_k = k

    root.label += min_k
    for child in root.children:
        update_labels_helper(child, min_k, character)


def update_labels_helper(local_root, parent_k, character):
    min_key, min_value = get_min_key_value(local_root, parent_k, character)

    # Update label
    if not local_root.is_leaf:
        local_root.label += min_key

    # Update distances
    if parent_k != min_key:
        local_root.distance_to_parent += 1

    # Recursively update children
    for child in local_root.children:
        update_labels_helper(child, min_key, character)


def small_parsimony(T, character):
    for i in range(T.sequence_length):
        for node in T.nodes.values():
            node.is_sk_processed = False
            if node.is_leaf:
                node.is_sk_processed = True
                for k in character:
                    if node.label[i] == k:
                        node.sk[k] = 0
                    else:
                        node.sk[k] = float('inf')

        # Assign scores for each base pair
        ripe_node = T.get_ripe_node()  # Inefficient, but who's ever going to know? :)
        root = None
        while ripe_node is not None:
            ripe_node.is_sk_processed = True
            for k in character:
                ripe_node.sk[k] = get_min_score(ripe_node, k, character)
            root = ripe_node
            ripe_node = T.get_ripe_node()

        # Use scores to get inner-node nucleotide
        update_labels(root, character)


def save_output(output_file_path, T):
    out_string = ""
    out_string += str(T.get_parsimony_score()) + "\n"
    edges = T.get_edges()
    for edge in edges:
        first, second, weight = edge
        out_string += str(first) + "->" + str(second) + ":" + str(weight) + "\n"
        out_string += str(second) + "->" + str(first) + ":" + str(weight) + "\n"

    with open(output_file_path, 'w+') as out_file:
        out_file.write(out_string)


def mr_gorbachev_tear_out_this_root(T):
    child1 = T.root.children[0]
    child2 = T.root.children[1]

    child1.parent = child2
    child2.parent = None
    child2.children.append(child1)

    child1.distance_to_parent += child2.distance_to_parent
    child2.distance_to_parent = 0


def get_tree_strings(T):
    out_string = ""
    for node in T.nodes.values():
        for link in node.links:
            out_string += node.label + "->" + link.label + "\n"

    return out_string


if __name__ == '__main__':
    input_file_path = "input.txt"
    output_file_path = "output.txt"
    character = ['A', 'C', 'G', 'T']

    edge, T = build_simple_tree(input_file_path)
    first = T.nodes[edge[0]]
    second = T.nodes[edge[1]]

    for link in first.links:
        if link != second:
            first.children.append(link)
    for link in second.links:
        if link != first:
            second.children.append(link)

    out_tree_strings = []
    for i in range(2):
        first_swap_child = first.children.pop()
        first.links.remove(first_swap_child)
        first_swap_child.links.remove(first)

        second_swap_child = second.children[0]
        second.children.remove(second_swap_child)
        second.links.remove(second_swap_child)
        second_swap_child.links.remove(second)

        first.children.append(second_swap_child)
        first.links.append(second_swap_child)
        second_swap_child.links.append(first)

        second.children.append(first_swap_child)
        second.links.append(first_swap_child)
        first_swap_child.links.append(second)

        out_tree_strings.append(get_tree_strings(T))

    with open(output_file_path, 'w+') as out_file:
        for string in out_tree_strings:
            out_file.write(string + "\n")
