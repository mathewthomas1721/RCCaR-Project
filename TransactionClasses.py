class Transaction :

    def __init__(self, tNo, tick):
        self.startTime = tick
        self.tNo = tNo
        self.exLocks = {}
        self.sharedLocks = {}
        self.endTime = -1 #use to

    def endTranscation(self,tick,sites):

        for site in self.exLocks:
            currSite = sites[site]
            for variable in self.exLocks[site]:
                currSite.exLocks[variable] = -1

        for site in self.sharedLocks:
            currSite = sites[site]
            for variable in self.sharedLocks[site]:
                currSite.sharedLocks[variable].remove(self.tNo)
        self.exLocks = {}
        self.sharedLocks = {}
        self.endTime = tick        
        print "Locks Released"
