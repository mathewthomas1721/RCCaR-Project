'''
Replicated Concurrency Control and Recovery Project
Advanced Datbase Systems - Prof. Dennis Shasha

MATHEW THOMAS
N15690387
'''
'''
class Variable:

Each instance of Variable corresponds to a variable stored in the database

'''

class Variable:
    def __init__(self, index, numSites):
        self.index = index
        self.val = 10 * index
        self.locs = []
        for i in range(1,numSites+1):
            if index % 2 == 0:
                self.locs.append(i)
            elif i == (1 + (index % 10)):
                self.locs.append(i)
