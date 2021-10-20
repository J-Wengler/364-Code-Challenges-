class Tree:
    def __init__(self, T):
        self.T = T

    def __repr__(self):
        r_string = ''
        for i in range(len(self.T)):
            r_string = r_string + self.T[i].__repr__() + '\n'
        return r_string