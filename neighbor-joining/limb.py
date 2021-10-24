class Limb:
    def __init__(self, start, end, length):
         self.start = start
         self.end = end
         self.length = length

    def out_str(self):
        out_str = "{:d}->{:d}:{:.3f}\n".format(self.start, self.end, self.length)
        return out_str

    def get_start(self):
        return self.start


        
