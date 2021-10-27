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
    T = {}
    cur_num = 0
    while True:
        line = input_file.readline()
        if not line:
            break
        else:
            nodes = line.rstrip().split("->")
            #print(nodes)
            label_one = nodes[0]
            label_two = nodes[1]
            if label_one not in T.keys():
                T[label_one] = Node(label_one)
                if label_one.isnumeric():
                    T[label_one].label = ""
            if label_two not in T.keys():
                T[label_two] = Node(label_two)
                if label_two.isnumeric():
                    T[label_two].label = ""
            T[label_one].links.append(T[label_two])
            #T[label_two].links.append(T[label_one])
            
    input_file.close()
    return Tree(T)