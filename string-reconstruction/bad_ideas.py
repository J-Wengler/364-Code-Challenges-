# Thoughts on taking a list of patterns and forming an adjacency list

def get_start(read, k):
    return read[0:k - 1]


def get_end(read, k):
    return read[len(read) - k + 1:]


def print_adjacencies(adjacency_list):
    out_file = open("/Users/jameswengler/output.txt", "w+")
    for adjacency in adjacency_list:
        out_str = adjacency + " -> " + ','.join(adjacency_list[adjacency]) + '\n'
        out_file.write(out_str)


if __name__ == '__main__':
    input_file = open('/Users/jameswengler/Downloads/input.txt')

    k = int(input_file.readline())
    #string = input_file.readline()

    nodes = []

    #for i in range(len(string) - k + 2):
        #nodes.append(string[i:i+k-1])

    edges = input_file.read().splitlines() 
    adjacency_list = {}

    #for i in range(len(string) - k + 1):
        #edges.append(string[i:i + k])

    # for i in range(len(nodes)):
    #

    for edge in edges:
        prefix = get_start(edge, k)
        suffix = get_end(edge, k)
        if prefix not in adjacency_list.keys():
            adjacency_list[prefix] = []
        adjacency_list[prefix].append(suffix)


    #print(nodes)
    #print(edges)

    print(adjacency_list)
    quit(1)
    print_adjacencies(adjacency_list)
    input_file.close()
