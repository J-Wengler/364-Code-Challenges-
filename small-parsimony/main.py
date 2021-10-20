import numpy as np

from buildtreefromfile import buildtreefromfile

def small_parsimony(T, character):
    # note this extra for loop will allow us to
    # iterate over each character in the genome
    # so we can operate on the tree as if the 
    # nodes were labeled with just one character
    for i in range(len(T.T[0].label)):
        for j in range(len(T.T)):
            T.T[j].tag = 0
            if len(T.T[j].children) == 0:
                T.T[j].tag = 1
                for k in character:
                    if T.T[j].label[i] == k:
                        T.T[j].sk[k] = 0
                    else: 
                        T.T[j].sk[k] = float('inf')
        ##########################                        
        # next part should go here
        ##########################
    # you are welcome to return whatever you want
    # this was just how I did it for debugging
    return T 

T = buildtreefromfile('toyinput.txt')

character = ['A', 'C', 'G', 'T']

# I added __repr__'s to both node
# and tree for easy debugging
print(small_parsimony(T, character))




