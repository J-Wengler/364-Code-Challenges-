from typing import Pattern

def get_symbol(lst):
    return lst[0]

def build_last_to_first(last_column):
    # this function should be used to build a
    # dict last_to_first where the keys are 
    # indexes in the last_column mapped to 
    # values that are the corresponding indexes
    # in the first_column
    last_to_first = {}
    symbol_counts = {}
    modified_last_column = []
    i = 0
    for symbol in last_column:
        if symbol not in symbol_counts.keys():
            symbol_counts[symbol] = 1
        else:
            symbol_counts[symbol] += 1
        modified_last_column.append([symbol, symbol_counts[symbol], i])
        i += 1
    modified_first_column = sorted(modified_last_column, key=get_symbol)
    for i in range(len(modified_first_column)):
        last_to_first[modified_first_column[i][2]] = i
    return last_to_first

def bw_matching(last_column, pattern, last_to_first):
    top = 0
    bottom = len(last_column) - 1
    while top <= bottom:
        if not pattern:
            symbol = pattern[-1]
            pattern = pattern[:-1]
            if symbol in last_column:
                top_index = last_column.index(symbol)
                bottom_index = len(last_column) - 1 - last_column[::-1].index(symbol)
                top = last_to_first[top_index]
                bottom = last_to_first[bottom_index]
            else:
                return 0
        else:
            return bottom - top + 1

def main():
    input_file = "input.txt"

    with open (input_file, 'r') as in_file:
        last_column = in_file.readline().strip()
        patterns = in_file.readline().split()

    # I do not think this is working LOL
    last_to_first = build_last_to_first(last_column)

    for pattern in patterns:
        print(bw_matching(last_column, pattern, last_to_first), end=' ')

if __name__ == "__main__":
    main()