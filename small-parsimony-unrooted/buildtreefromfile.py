from node import Node
from tree import Tree

def buildtreefromfile(file_name):
    input_file = open(file_name, 'r+')
    n = int(input_file.readline().split()[0])
    i = 0
    T = {}
    while True:
        line = input_file.readline()
        if not line:
            break
        else:
            nodes = line.rstrip().split("->")
            first_num = int(nodes[0])
            second_num = None
            label = None
            if i < n:
                second_num = i
                label = nodes[1]
            else:
                second_num = int(nodes[1])
            if first_num not in T.keys():
                T[first_num] = Node(first_num)
            if second_num not in T.keys():
                T[second_num] = Node(second_num)
                if label:
                    T[second_num].label = label
            T[first_num].children.append(T[second_num])
            T[second_num].parent = T[first_num]
        i += 1
    input_file.close()
    return Tree(T)


def build_unrooted_tree(file_name):
    input_file = open(file_name, 'r+')
    n = int(input_file.readline().split()[0])
    i = 0
    T = {}
    while True:
        line = input_file.readline()
        if not line:
            break
        else:
            nodes = line.rstrip().split("->")
            if (nodes[0].isnumeric() == False):
                continue
            first_num = int(nodes[0])
            second_num = None
            label = None
            if i < n:
                second_num = i
                label = nodes[1]
            else:
                second_num = int(nodes[1])
            if first_num not in T.keys():
                T[first_num] = Node(first_num)
            if second_num not in T.keys():
                T[second_num] = Node(second_num)
                if label:
                    T[second_num].label = label
            T[first_num].children.append(T[second_num])
            T[second_num].parent = T[first_num]
        i += 1
    input_file.close()
    return Tree(T)