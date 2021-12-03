from os import remove
from buildtreefromfile import build_simple_tree
from node import Node


# Gets the best, lowest-parsimony score possible for a given parent (ripe_node) to
# achieve a given nucleotide (k).
def get_min_score(ripe_node, k, character):
    left = ripe_node.children[0]
    right = ripe_node.children[1]

    min_key_left, min_value_left = get_min_key_value(left, k, character)
    min_key_right, min_value_right = get_min_key_value(right, k, character)

    return min_value_left + min_value_right

#def assign_node_unrooted_Tree(T):

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

def remove_root(T):
    child1 = T.root.children[0]
    child2 = T.root.children[1]

    child1.parent = child2
    child2.parent = None
    child2.children.append(child1)

    child1.distance_to_parent += child2.distance_to_parent
    child2.distance_to_parent = 0
    del T.T['root']

    return T

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
    # note this extra for loop will allow us to
    # iterate over each character in the genome
    # so we can operate on the tree as if the 
    # nodes were labeled with just one character
    for i in range(len(T.T[next(iter(T.T))].label)):
        for j in T.T.keys():
            T.T[j].tag = 0
            if len(T.T[j].children) == 0:
                T.T[j].tag = 1
                for k in character:
                    if T.T[j].label[i] == k:
                        T.T[j].sk[k] = 0
                    else: 
                        T.T[j].sk[k] = float('inf')

        # Assign scores for each base pair
        ripe_node = T.get_ripe_node()  # Inefficient, but who's ever going to know? :)
        root = None
        while ripe_node is not None:
            ripe_node.tag = 1
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

input_file_path = "/Users/jameswengler/BIO 364/364-Code-Challenges-/small-parsimony-unrooted/input.txt"
output_file_path = "/Users/jameswengler/BIO 364/364-Code-Challenges-/small-parsimony-unrooted/output.txt"
character = ['A', 'C', 'G', 'T']

##### Unrooted Tree Code Below #####

# Build an unrooted tree from the data then root it
T = build_simple_tree(input_file_path)
# Run small parsimony on the new rooted tree
small_parsimony(T, character)
# Remove the root
T = remove_root(T)
#Find all the edges of labels of the re-unrooted tree
save_output(output_file_path, T)

