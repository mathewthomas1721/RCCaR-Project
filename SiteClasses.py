'''
class Site

Each instance of Site corresponds to a site.

Data Items :

index : Site index
vars : Variables stored at site
vals : Values of variables stored at site
exLocks : Exclusive locks on variables at site
sharedLocks : Shared locks on variables at site
alive : Whether site is alive or not :
        1 -> alive
        -1 -> not alive
        0 -> non-replicated items available
nonReplicatedVars : list of non-replicated variables at site
replicatedVars : list of replicated variables at site
unavailable : list of unavailable variables at site       
'''

class Site:

    def __init__(self, index, numVar,varVals):
        self.index = index
        self.vars = []
        self.vals = {}
        self.exLocks = {}
        self.sharedLocks = {}
        self.alive = 1
        self.nonReplicatedVars = []
        self.replicatedVars = []
        self.unavailable = []
        for i in range(1,numVar+1):
            if i%2 == 0:
                self.vars.append(i)
                self.replicatedVars.append(i)
                self.vals[i] = varVals[i].val
                self.exLocks[i] = -1
                self.sharedLocks[i] = []

            elif (1 + (i%10)) == index:

                self.vars.append(i)
                self.nonReplicatedVars.append(i)
                self.vals[i] = varVals[i].val
                self.exLocks[i] = -1
                self.sharedLocks[i] = []
