import numpy as np
from limb import Limb
import collections

with open("/Users/jameswengler/BIO 364/364-Code-Challenges-/neighbor-joining/input.txt", "r") as in_file:
    n = in_file.readline()
    distance_matrix = np.loadtxt(in_file)
    
def row_sum(x, data):
    row_sum = data.sum(axis = 0)[x]
    return row_sum

def col_sum(y, data):
    col_sum = data.sum(axis = 1)[y]
    return col_sum 



def transform_matrix(data):
    n, num_cols = data.shape
    temp_matrix = np.zeros((n, n))
    net_divergence = data.sum(axis=0)
    # print(data)
    # print(net_divergence)
    for x in range(0, n):
        for y in range(0,n):
            if x == y:
                continue
            row_sum_x = row_sum(x, data)
            col_sum_y = col_sum(y, data)
            temp_matrix[x][y] = (n - 2) * data[x][y] - col_sum_y - row_sum_x

    return temp_matrix

def find_matrix_mins(data):
    n, num_cols = data.shape
    temp_min = 1000
    temp_x = 0
    temp_y = 0
    for x in range(0, n):
        for y in range(0,n):
            if data[x][y] < temp_min and x != y:
                temp_min = data[x][y]
                temp_x = x
                temp_y = y
    return temp_x, temp_y, temp_min

def updateArray(D, i, j):
    n, num_col = D.shape
    new_row = np.array([(1/2)*(D[k,i] + D[k,j] - D[i,j]) for k in range(0,n)])
    new_row = np.delete(new_row, [i,j])
    new_col = np.insert(new_row, 0, 0)
    new_col = np.reshape(new_col, (len(new_col), 1))
    D = np.delete(D, [i,j], axis = 0)
    D = np.delete(D, [i,j], axis = 1)
    D = np.vstack([new_row, D])
    D = np.hstack([new_col, D])
    return D
    





def neighbor_join(data, limb_list, node_counter, og_num, labels):
    n, num_cols = data.shape
    if n == 2:
        base_case_limb_1 = Limb(labels[0], labels[1], data[0,1])
        base_case_limb_2= Limb(labels[1], labels[0], data[0,1])
        limb_list.append(base_case_limb_1)
        limb_list.append(base_case_limb_2)
        return data
    d_star = transform_matrix(data)
    i,j, d_star_i_j = find_matrix_mins(d_star)
    m = og_num + node_counter
    node_counter += 1
    change = (row_sum(i, data) - col_sum(j, data)) / (n-2)
    limb_length_i = (data[i][j] + change)*(.5)
    limb_length_j = (data[i][j] - change)*(.5)
    new_limb_i_to_m = Limb(labels[i], m, limb_length_i)
    #print(new_limb_i_to_m.out_str())
    new_limb_j_to_m = Limb(labels[j] , m, limb_length_j)
    
    #print(new_limb_j_to_m.out_str())
    new_limb_m_to_i = Limb(m, labels[i], limb_length_i)
    
    #print(new_limb_m_to_i.out_str())
    new_limb_m_to_j = Limb(m , labels[j], limb_length_j)
    #print(new_limb_m_to_j.out_str())
    limb_list.append(new_limb_i_to_m)
    limb_list.append(new_limb_j_to_m)
    limb_list.append(new_limb_m_to_i)
    limb_list.append(new_limb_m_to_j)
    labels = np.delete(labels, [i,j])
    labels = np.insert(labels, 0, m)
    D = updateArray(data, i, j)
    T = neighbor_join(D, limb_list, node_counter, og_num, labels)
    return T

    
    
    
ll = []
labels = list(range(0,int(n)))
neighbor_join(distance_matrix, ll, 0, int(n), labels)
# print(ll)
out_dict = {}
for limb in ll:
    if limb.get_start() not in out_dict.keys():
        out_dict[limb.get_start()] = [limb]
    else:
        out_dict[limb.get_start()].append(limb)
        

od = collections.OrderedDict(sorted(out_dict.items()))

with open("/Users/jameswengler/BIO 364/364-Code-Challenges-/neighbor-joining/output.txt", "w+") as output:
    for k, v in od.items():
        limb_list = od[k]
        for limb in limb_list:
            output.write(limb.out_str())
    #print(limb.out_str())