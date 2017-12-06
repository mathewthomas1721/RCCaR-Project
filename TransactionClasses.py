'''
Replicated Concurrency Control and Recovery Project
Advanced Datbase Systems - Prof. Dennis Shasha

MATHEW THOMAS
N15690387
'''
'''
class Transaction

Maintains information about individual transactions.

startTime : Time at which transaction starts
tNo : Transaction Number
exLocks : All exclusive locks that the transaction holds
sharedLocks : All shared locks that the transaction holds
opList : All operations that the transaction has performed
endTime : Time at which the transaction ends, ie, aborts or commits
RO : 1 if transaction is ReadOnly, -1 if not
ReadValues : Values of variables when the transaction starts. Used only for
ReadOnly transactions

'''

'''
checkDone()

Checks if the transaction has terminated

Output : Returns False if the transaction is still executing
Returns True if the transaction has terminated
'''

'''
endTransaction(self,tick,sites)

Terminates a transaction
'''

'''
commit(self,tick,sites)

Commits all operations carried out by the transaction to the database
'''
class Transaction :

    def __init__(self, tNo, tick):
        self.startTime = tick
        self.tNo = tNo
        self.exLocks = {}
        self.sharedLocks = {}
        self.opList = []
        self.endTime = -1 #use to
        self.RO = -1
        self.ReadValues = {}



    def checkDone():
        if self.endTime == -1:
            return False
        else:
            return True



    def endTransaction(self,tick,sites):
        #print("ENDING TRANSACTION T" + str(self.tNo))
        for site in self.exLocks:
            currSite = sites[site-1]
            for variable in self.exLocks[site]:
                currSite.exLocks[variable] = -1
        #print self.sharedLocks
        for site in self.sharedLocks:
            currSite = sites[site-1]
            #print currSite.index
            #print site
            #print sites[site-1].index
            for variable in self.sharedLocks[site]:
                #print site, currSite.sharedLocks
                #print variable
                currSite.sharedLocks[variable].remove(self.tNo)
        self.exLocks = {}
        self.sharedLocks = {}
        self.endTime = tick
        #print "Locks Released"



    def commit(self,tick,sites):

        for op in self.opList:
            variable = op[0]
            siteIndex = op[1] - 1
            value = op[2]
            sites[siteIndex].vals[variable] = value
        self.endTransaction(tick,sites)
