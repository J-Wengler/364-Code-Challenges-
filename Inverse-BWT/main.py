import numpy as np

input_file = open("/Users/jameswengler/BIO 364/364-Code-Challenges-/Inverse-BWT/input.txt", 'r')
out_file = open("/Users/jameswengler/BIO 364/364-Code-Challenges-/Inverse-BWT/output.txt", 'w+')
bwt = input_file.readline()

def split_word(word):
    return [char for char in word]

def sort_rows(my_array):
    flattened = my_array.tolist()
    sorted_list = sorted(flattened)
    sorted_array = np.array(sorted_list)
    return sorted_array

def get_string_from_array(my_array):
    for row in my_array:
        if row[len(row) - 1] == "$":
            return(''.join(row))


def undoBWT(bwt):
    og_bwt = split_word(bwt)
    first_col = sorted(bwt)
    my_array = np.column_stack((og_bwt, first_col))
    sorted_array = sort_rows(my_array)
    

    for i in (range(len(bwt) - 2)):
        new_array = np.column_stack((og_bwt, sorted_array))
        sorted_array = sort_rows(new_array)
    
    final_string = get_string_from_array(sorted_array)
    return(final_string)

output = undoBWT(bwt)
out_file.write(output)




