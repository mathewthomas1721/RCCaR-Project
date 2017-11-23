class Site:

    def __init__(self, index, numVar,varVals):
        self.index = index
        self.vars = []
        self.vals = {}
        self.locks = {}
        self.sharedLocks = {}
        for i in range(1,numVar+1):
            if (1 + (i%10)) == index:
                self.vars.append(i)
                self.vals[i] = varVals[i].val
                self.locks[i] = -1
                self.sharedLocks[i] = []
            elif i%2 == 0:
                self.vars.append(i)
                self.vals[i] = varVals[i].val
                self.locks[i] = -1
                self.sharedLocks[i] = []
