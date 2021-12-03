from os import remove
from typing import Tuple
from buildtreefromfile import *
from node import Node
import copy


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

def parse_from_root_bad(parent_node):
    for child in parent_node.links:
        parent_node.children.append(child)
        child.parent = parent_node
        child.links.remove(parent_node)
        parse_from_root(child)

def parse_from_root(parent_node):
    #parent_node.parse_links_copy = copy.deepcopy(parent_node.links)
    for child in parent_node.links:
        #print(f"CHILD : {child}")
        if child not in parent_node.children:
            parent_node.children.append(child)
        child.parent = parent_node
        #child.parse_links_copy = copy.deepcopy(child.links)
        child.links.remove(parent_node)
        parse_from_root(child)


def dict_get_links(my_dict):
    total_links = 0
    for node in my_dict.values():
        total_links += len(node.links)
    return(total_links)

def reset_links(T):
    for node in T.values():
        node.links = []

def rebuild_links(T):
    reset_links(T)
    for node in T.values():
        if node.parent is not None:
            if node.parent not in node.links:
                node.links.append(node.parent)
        for child in node.children:
            if child not in node.links:
                node.links.append(child)
    

def make_root_bad(T, left, right):
    root = Node()
    T["root"] = root

    left.links.remove(right)
    right.links.remove(left)

    root.children.append(left)
    root.children.append(right)

    left.parent = root
    right.parent = root
    left.links.append(root)
    right.links.append(root)

    parse_from_root(left)
    parse_from_root(right)

    return T, root

def make_root(T, left, right):
    root = Node()
    T["root"] = root

    left.links.remove(right)
    right.links.remove(left)

    root.children.append(left)
    root.children.append(right)

    left.parent = root
    right.parent = root
    left.links.append(root)
    right.links.append(root)
    root.links.append(right)
    root.links.append(left)
    #print(f"PRE PARSE : {dict_get_links(T)}")
    parse_from_root(left)
    print(f"AFTER PARSE : {dict_get_links(T)}")
    rebuild_links(T)
    #print(T)

    print(f"AFTER LEFT : {dict_get_links(T)}")
    #print(root)
    #print(right)
    parse_from_root(right)
    rebuild_links(T)
    #print(f"AFTER RIGHT : {dict_get_links(T)}")

    return T,root

def remove_root(T):
    child1 = T.root.children[0]
    child2 = T.root.children[1]

    child1.parent = child2
    child2.parent = None
    child2.children.append(child1)

    child1.links.append(child2)
    child2.links.append(child1)
    if T.root in child1.links:
        child1.links.remove(T.root)
    if T.root in child2.links:
        child2.links.remove(T.root)


    # child1.links.remove(T.root)
    # child2.links.remove(T.root)

    child1.distance_to_parent += child2.distance_to_parent
    child2.distance_to_parent = 0
    del T.T['root']
    T.root = None

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
    #len(T.T[next(iter(T.T))].label)
    for i in range(8):
        for j in T.T.keys():
            T.T[j].tag = 0
            if T.T[j].is_leaf:
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
            #print(ripe_node)

        # Use scores to get inner-node nucleotide
        
        update_labels(root, character)

def save_output(T):
    out_string = ""
    out_string += str(T.sp) + "\n"
    edges = T.get_edges()
    for edge in edges:
        first, second, weight = edge
        out_string += str(first) + "->" + str(second) + ":" + str(weight) + "\n"
        out_string += str(second) + "->" + str(first) + ":" + str(weight) + "\n"
    return out_string

input_file_path = "/Users/jameswengler/BIO 364/364-Code-Challenges-/NNIN/input.txt"
output_file_path = "/Users/jameswengler/BIO 364/364-Code-Challenges-/NNIN/output.txt"
character = ['A', 'C', 'G', 'T']

def find_index(node, links):
    for link in links:
        if node == link:
            print("Found it!")

##### Unrooted Tree Code Below #####

def swap_first(T, first, second):
    for link in first.links:
        if link != second:
            first.swap_children.append(link)

    for link in second.links:
        if link != first:
            second.swap_children.append(link)

    first_swap_child = first.swap_children.pop()
    first.links.remove(first_swap_child)
    first_swap_child.links.remove(first)

    second_swap_child = second.swap_children[0]
    second.swap_children.remove(second_swap_child)
        
    second.links.remove(second_swap_child)
    second_swap_child.links.remove(second)

    first.swap_children.append(second_swap_child)
    first.links.append(second_swap_child)
    second_swap_child.links.append(first)

    second.swap_children.append(first_swap_child)
    second.links.append(first_swap_child)
    first_swap_child.links.append(second)
    return T

def swap_second(T, first, second):
    print(f"TREE LENGHTS : {T.get_num_links()}")
    first.swap_children = []
    for link in first.links:
        if link != second:
            first.swap_children.append(link)
    print(f"FSC : {len(first.swap_children)}")

    second.swap_children = []
    for link in second.links:
        if link != first:
            second.swap_children.append(link)
    print(f"SSC : {len(second.swap_children)}")

    #first_swap_child = first.swap_children.pop()
    first_swap_child = first.swap_children[1]
    first.swap_children.remove(first_swap_child)
    first.links.remove(first_swap_child)
    first_swap_child.links.remove(first)

    second_swap_child = second.swap_children[1]
    second.swap_children.remove(second_swap_child)
        
    second.links.remove(second_swap_child)
    second_swap_child.links.remove(second)

    first.swap_children.append(second_swap_child)
    first.links.append(second_swap_child)
    second_swap_child.links.append(first)

    second.swap_children.append(first_swap_child)
    second.links.append(first_swap_child)
    first_swap_child.links.append(second)
    return T

    
    




def swap(T, first, second):
    #edge, T = build_simple_tree(input_file_path)    
    #first = T.nodes[edge[0]]
    #second = T.nodes[edge[1]]
    #print(first)

    swap_copy_one = copy.deepcopy(T)
    swap_copy_two = copy.deepcopy(T)

    first_swap = swap_first(swap_copy_one, first, second)
    second_copy = copy.deepcopy(first_swap)
    second_swap = swap_second(swap_copy_two, first, second)
    return [first_swap, second_swap]

def get_tuples_neighboring_nodes(T):
    tuples = []
    for node in T.T.values():
        if not node.is_leaf:
            for link in node.links:
                if not link.is_leaf:
                    temp_tuple = [node, link]
                    reverse_tuple = [link, node]
                    if temp_tuple not in tuples and reverse_tuple not in tuples:
                        tuples.append(temp_tuple)
    return tuples

def root_run_sp_unroot(T):
    #T.reset_tree()
    temp_node = None
    for node in T.T.values():
        temp_node = node
        break
    #print(f"Number of nodes (pre): {len(T.T.values())}")
    #print(f"PRE MAKE ROOT : {T.get_num_links()}")
    if T.root == None:
        T.T,root = make_root(T.T, temp_node, temp_node.links[0])
    #print(f"Number of nodes (post): {len(T.T.values())}")
        T.root = root
    characters = ['A', 'C', 'G', 'T']
    small_parsimony(T, characters)
    #T.get_num_links()
    #print(f"PRE REMOVE ROOT : {T.get_num_links()}")
    sp_score = T.get_parsimony_score()
    T = remove_root(T)
    #print(f"POST REMOVE ROOT : {T.get_num_links()}")
    
    T.sp = sp_score
    out_str = save_output(T)
    #T.reset_family()
    #print(f"Number of nodes (return): {len(T.T.values())}")
    return T, sp_score, out_str

def print_tree_links(T):
    print()
    for node in T.T.values():
        print(len(node.links))

def NNIN(input_file, out_file):
    score = float('inf')
    first_unrooted_tree = build_simple_tree_from_file(input_file)
    current_tree, new_score, out_str = root_run_sp_unroot(first_unrooted_tree)
    i = 0
    with open(out_file, "w+") as output:
        while new_score < score:
            print(f"Iteration {i} -> {new_score}")
            output.write(out_str)
            output.write('\n')
            i += i + 1
            score = new_score
            current_tree.reset_tree()
            neighbors = get_tuples_neighboring_nodes(current_tree)
            for neighbor in neighbors:
                score_to_dict = {}
                temp_to_swap = copy.deepcopy(current_tree)
                print(temp_to_swap.get_num_links())
                temp_to_swap.reset_tree()
                print(temp_to_swap.get_num_links())
                #print(temp_to_swap)
                two_options = swap(temp_to_swap, neighbor[0], neighbor[1])
                tree_1, score_1, out_1 = root_run_sp_unroot(two_options[0])
                tree_2, score_2, out_2 = root_run_sp_unroot(two_options[1])
                score_to_dict[score_1] = (tree_1, out_1)
                score_to_dict[score_2] = (tree_2, out_2)
            for temp_score in score_to_dict.keys():
                if temp_score < score:
                    new_score = temp_score
                    out_str = score_to_dict[temp_score][1]
                    current_tree = score_to_dict[temp_score][0]
                    #print(current_tree)
                    #print("----------------------")
                    #print(current_tree.get_num_links())
                    #current_tree.reset_tree()
                    #print(current_tree)
                    #print(current_tree.get_num_links())
                    break



def NNIN_bad(input_file, out_file):
    score = float('inf')
    first_unrooted_tree = build_simple_tree(input_file)
    #print(first_unrooted_tree)
    #print("-----------------------------")
    #neighbors = get_tuples_neighboring_nodes(first_unrooted_tree)
    #current_tree = copy.deepcopy(first_unrooted_tree)
    current_tree, new_score, out_str = root_run_sp_unroot(first_unrooted_tree)
    #print(initial_tree)
    #quit(1)
    i = 0
    with open(out_file, "w+") as output:
        while new_score < score:
            print(f"Iteration {i} -> {new_score}")
            output.write(out_str)
            output.write('\n')
            #print(f"TREE STRING : {tree_string}")
            #output.write(tree_string)
            i += i + 1
            #print(new_score)
            score = new_score
            #copy_to_swap = copy.deepcopy(current_tree)
            neighbors = get_tuples_neighboring_nodes(current_tree)
            for neighbor in neighbors:
                current_tree.reset_family()
                two_options = swap(current_tree, neighbor[0], neighbor[1])
                #try:
                tree_1, score_1, out_1 = root_run_sp_unroot(two_options[0])
                #except:
                #    score_1 = float('inf')
                #try:
                #print("-----------------------------------------------------")
                #print(two_options[1])
                tree_2, score_2, out_2 = root_run_sp_unroot(two_options[1])
                #except:
                #    score_2 = float('inf')
                if score_1 < score:
                    current_tree = tree_1
                    new_score = score_1
                    out_str = out_1
                    break
                if score_2 < score:
                    current_tree = tree_2
                    new_score = score_2
                    out_str = out_2
                    break
                
                
            current_tree.reset_family()
        print("All Done!")
    
    # winning_tree = None
    # for tree in trees_to_scores.keys():
    #     if trees_to_scores[tree] < score:
    #         score = trees_to_scores[tree]
    #         winning_tree = tree
    
        

    


NNIN(input_file_path, output_file_path)

print(len("AGCTACCCATCATTTTTGCGAGCATACGGCCTCCCTCCTG"))




# Build an unrooted tree from the data then root it
#T = build_simple_tree(input_file_path)
# Run small parsimony on the new rooted tree
#small_parsimony(T, character)
# Remove the root
#T = remove_root(T)
#Find all the edges of labels of the re-unrooted tree
#save_output(output_file_path, T)

