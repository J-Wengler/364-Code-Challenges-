import collections

in_file = open("/Users/jameswengler/BIO 364/364-Code-Challenges-/suffix-array/input.txt")
out_file = open("/Users/jameswengler/BIO 364/364-Code-Challenges-/suffix-array/output.txt", "w+")
pattern = in_file.readline()
unsorted_dict = {}
for num in range(len(pattern)):
    suffix = pattern[num:len(pattern)]
    unsorted_dict[suffix] = num
sorted_dict = collections.OrderedDict(sorted(unsorted_dict.items()))
for num in sorted_dict.values():
    out_file.write(f"{num} ")