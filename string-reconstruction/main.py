# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# To-Do List
# 1. Create node class 
# 2. Retrofit the old code for DB code to use the node class 
# 3. Function to find eulerian path in a DB graph
# 4. Takes a eulerian path and turns it into a genome
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from Graph import Graph

# Path to adjacency list
input_file = "/Users/jameswengler/Downloads/dataset_577139_6.txt"

test_graph = Graph(input_file)

test_graph.make_db_graph()
test_graph.print_nodes()
