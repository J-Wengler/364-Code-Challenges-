import numpy

def get_index_for_appearance(column, appearance, symbol):
    num_appearances = 0
    for i in range(len(column)):
        if column[i] == symbol:
            num_appearances += 1
        if num_appearances == appearance:
            return i

def get_num_appearances(column, i):
    num_appearances = 0
    search_symbol = column[i]
    for j in range(len(column)):
        if column[j] == search_symbol:
            num_appearances += 1
        if j == i:
            break
    return num_appearances

def count_occurences(symbol, line):
    count = 0
    for character in line:
        if symbol == character:
            count += 1
    return(count)

def count_function(count, symbol, i, character_set):
    #print(count)
    j = character_set.index(symbol)
    #print(f"CHARACTER SET : {character_set}\nJ : {j}\nSYMBOL : {symbol}\nI : {i}\nSIZE : {count.shape}")
    return int(count[i,j])

def generate_count(last_column):
    character_set = list(set(last_column))
    count = numpy.zeros((len(last_column) + 1, len(character_set)))
    for i in range(len(last_column) + 1):
        spliced_list = last_column[:i]
        for j in range(len(character_set)):
            cur_char = character_set[j]
            count[i,j] = count_occurences(cur_char, spliced_list)
    return count, character_set



        
    # count = {}
    # for symbol in character_set:
    #     count_list = []
    #     for i in range(len(last_column) + 1):
    #         cur_count = 0
    #         for j in range(i):
    #             spliced_list = last_column[:j + 1]
    #             cur_count = count_occurences(symbol, spliced_list)
    #         count_list.append(cur_count)
            
    #     count[symbol] = count_list
    #return count

def build_last_to_first(last_column):
    last_to_first = {}
    first_column = ''.join(sorted(last_column))
    for i in range(len(last_column)):
        last_to_first[i] = get_index_for_appearance(first_column, get_num_appearances(last_column, i), last_column[i])
    return last_to_first

def first_occurence(symbol, last_column):
    first_col = sorted(last_column)
    for i  in range(len(first_col)):
        if first_col[i] == symbol:
            return i

def generate_first_occurence(last_column):
    first_col = sorted(last_column)
    characters = ''.join(set(first_col))
    first_occurence = {}
    for character in characters:
        for i in range(len(first_col)):
            if first_col[i] == character:
                if i is not 0:
                    first_occurence[character] = i
                else:
                    first_occurence[character] = i
                break
    return first_occurence


def bw_matching(last_column, pattern, count, first_occurence, character_set):
    top = 0
    bottom = len(last_column) - 1
    while top <= bottom:
        if pattern:
            symbol = pattern[-1]
            pattern = pattern[:-1]
            if symbol in last_column[top: bottom + 1]:
                top = first_occurence[symbol] + count_function(count, symbol, top, character_set)
                bottom = first_occurence[symbol] + count_function(count, symbol, bottom + 1, character_set) - 1
            else:
                return 0
                
        else:
            return bottom - top + 1
           

def main():
    input_file = "/Users/jameswengler/BIO 364/364-Code-Challenges-/BWT-Matching/Better-BWT-Matching/input.txt"

    with open (input_file, 'r') as in_file:
        last_column = in_file.readline().strip()
        patterns = in_file.readline().split()

    count,character_set = generate_count(last_column)
    first_occurence = generate_first_occurence(last_column)

    out_str = ""
    for pattern in patterns:
        out_str += f"{bw_matching(last_column, pattern, count, first_occurence, character_set)} "
        #print(bw_matching(last_column, pattern, count, first_occurence, character_set))

    print(out_str)

if __name__ == "__main__":
    main()