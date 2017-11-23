class Variable:
    def __init__(self, index, numSites):
        self.val = 10 * index
        self.locs = []
        for i in range(1,numSites+1):
            if index % 2 == 0:
                self.locs.append(i)
            elif i == (1 + (index % 10)):
                self.locs.append(i)
            
