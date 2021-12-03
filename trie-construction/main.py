from typing import Pattern
from trie import Trie

in_file = open("/Users/jameswengler/BIO 364/364-Code-Challenges-/trie-construction/input.txt")
pattern_line = in_file.readline()
patterns = pattern_line.split(" ")

myTrie = Trie()

myTrie.add_root()

myTrie.add_pattern("ATAGA")

for pattern in patterns:
    myTrie.add_pattern(pattern)

out_str = myTrie.__repr__()

out_file = open("/Users/jameswengler/BIO 364/364-Code-Challenges-/trie-construction/output.txt", "w+")
out_file.write(out_str)

