import time
import numpy as np

END_CHAR = '$'
ALPHABET = (END_CHAR, 'A', 'C', 'G', 'T')
A_COLS = {char: index for index, char in enumerate(ALPHABET)}
COUNTS_CHECKPOINT_DISTANCE = 100
SUFFIX_ARRAY_REDUCTION = 100


def add_counts_row(row_index, counts, bwt_position, bwt, checkpoint_distance):
    if row_index == 0:
        return
    for alpha_char, col_index in A_COLS.items():
        matching_chars = 0
        for i in range(checkpoint_distance):
            if bwt[bwt_position - 1 - i] == alpha_char:
                matching_chars += 1
        counts[row_index, col_index] = int(counts[row_index - 1, col_index]) + matching_chars


def get_counts(bwt, checkpoint_distance=1):
    num_rows = len(bwt) // checkpoint_distance + 1
    num_cols = len(ALPHABET)
    counts = np.array(np.zeros((num_rows, num_cols)))

    for bwt_position in range(len(bwt) + 1):
        if bwt_position % checkpoint_distance == 0:
            row_index = bwt_position // checkpoint_distance  # This should always be an integer value
            add_counts_row(row_index, counts, bwt_position, bwt, checkpoint_distance)

    return counts


def get_locations(first, last, partial_suffix_array, counts, bwt, first_occurrences):
    locations = []
    for i in range(first, last + 1):
        offset = 0
        while i not in partial_suffix_array.keys():
            num_chars_before = count(i, bwt, bwt[i], counts)
            i = first_occurrences[bwt[i]] + num_chars_before
            offset += 1
        location = partial_suffix_array[i] + offset
        locations.append(location)
    return sorted(locations)


def count(bwt_index, bwt, character, counts):
    nearest_checkpoint_index = bwt_index
    while nearest_checkpoint_index % COUNTS_CHECKPOINT_DISTANCE != 0:
        nearest_checkpoint_index -= 1
    counts_index = nearest_checkpoint_index // COUNTS_CHECKPOINT_DISTANCE

    extra_chars = 0
    for i in range(bwt_index - nearest_checkpoint_index):
        if bwt[bwt_index - 1 - i] == character:
            extra_chars += 1

    total_count = counts[counts_index, A_COLS[character]] + extra_chars
    return int(total_count)


def bw_matching(bwt, first_occurrences, counts, partial_suffix_array, read):
    top = 0
    bottom = len(bwt) - 1
    while top <= bottom:
        if len(read) > 0:
            symbol = read[-1]
            read = read[0:-1]

            top = int(first_occurrences[symbol] + count(top, bwt, symbol, counts))
            bottom = int(first_occurrences[symbol] + count(bottom + 1, bwt, symbol, counts) - 1)

            if top > bottom:
                return []
        else:
            return get_locations(top, bottom, partial_suffix_array, counts, bwt, first_occurrences)


def get_first_occurrences(alphabet, bwt):
    bwt_sorted = sorted(bwt)
    first_occurrences = {char: None for char in alphabet}
    for index, char in enumerate(bwt_sorted):
        if first_occurrences[char] is None:
            first_occurrences[char] = index
    return first_occurrences


def get_suffix_array(reference, reduction=1):
    # This first section is clearly much more space inefficient than the final result. But the more efficient algorithm
    # is apparently beyond the scope of this course. Yay!
    pair_list = []
    for i in range(len(reference)):
        pair_list.append((reference[i:], i))

    pair_list.sort()

    suffix_array = {}
    for index, str_pos_pair in enumerate(pair_list):
        if str_pos_pair[1] % reduction == 0:
            suffix_array[index] = str_pos_pair[1]

    return suffix_array


def get_bwt(reference):
    # This can also be done in linear time and space, but that's for another day.
    rotations = []
    for i in range(len(reference), 0, -1):
        cycled_string = reference[i:] + reference[0:i]
        rotations.append(cycled_string)

    rotations.sort()

    bwt = ""
    for rotation in rotations:
        bwt += rotation[len(rotation) - 1]

    return bwt


def get_output_string(read_match_pairs):
    output_string = ""
    for read, match_locations in read_match_pairs:
        match_string = ""
        for match_loc in match_locations:
            match_string += " " + str(match_loc)
        output_string += f"{read}:{match_string}\n"
    return output_string


def main():
    start = time.perf_counter()

    input_file = "input.txt"
    output_file = "output.txt"

    # Get input reference and reads
    with open(input_file, 'r') as in_file:
        reference = in_file.readline().strip() + END_CHAR
        # We'll just put all the reads into memory. Not memory efficient in real life. This disregard for the size
        # of reads continues throughout the code.
        reads = in_file.readline().split()

    # Prepare data structures using the reference
    partial_suffix_array = get_suffix_array(reference, reduction=SUFFIX_ARRAY_REDUCTION)
    bwt = get_bwt(reference)
    first_occurrences = get_first_occurrences(ALPHABET, bwt)
    checkpoint_counts = get_counts(bwt, checkpoint_distance=COUNTS_CHECKPOINT_DISTANCE)

    # Check for matches for each read
    read_match_pairs = []
    for read in reads:
        match_locations = bw_matching(bwt, first_occurrences, checkpoint_counts, partial_suffix_array, read)
        read_match_pairs.append((read, match_locations))

    # Output results
    output_string = get_output_string(read_match_pairs)
    with open(output_file, 'w') as out_file:
        out_file.write(output_string)

    print("Time: ", time.perf_counter() - start)


if __name__ == '__main__':
    main()
