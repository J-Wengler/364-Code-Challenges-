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


def build_last_to_first(last_column):
    last_to_first = {}
    first_column = ''.join(sorted(last_column))
    for i in range(len(last_column)):
        last_to_first[i] = get_index_for_appearance(first_column, get_num_appearances(last_column, i), last_column[i])
    return last_to_first


def bw_matching(last_column, pattern, last_to_first):
    top = 0
    bottom = len(last_column) - 1
    while top <= bottom:
        if pattern:
            symbol = pattern[-1]
            pattern = pattern[:-1]
            if symbol in last_column[top: bottom + 1]:
                top_index = last_column.index(symbol, top, bottom + 1)
                bottom_index = len(last_column) - 1 - last_column[::-1].index(symbol, len(last_column) - bottom - 1, len(last_column) - top + 1)
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

    last_to_first = build_last_to_first(last_column)

    for pattern in patterns:
        print(bw_matching(last_column, pattern, last_to_first), end=' ')

if __name__ == "__main__":
    main()