input_file = "input.txt"

with open (input_file, 'r') as in_file:
    reference = in_file.readline().strip()

rotations = []
for i in range(len(reference), 0, -1):
    cycled_string = reference[i:] + reference[0:i]
    rotations.append(cycled_string)

rotations.sort()

bwt = ""
for rotation in rotations:
    bwt += rotation[len(rotation) - 1]

print(bwt)
