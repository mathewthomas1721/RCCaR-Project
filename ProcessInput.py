from Checks import findAlive
def read(tNo,variable,sites,queue):
    allAlive = findAlive(variable,sites) #find all sites with variable
    for siteIndex in allAlive:
        if tNo != sites[siteIndex].exLocks[variable] or -1 == sites[siteIndex].exLocks[variable] : #check if the transaction has an exLock or there isn't an exLock
            sites[siteIndex].sharedLocks[variable].append(tNo) #add this transaction to shared locks
            return (sites[siteIndex].vals[variable], siteIndex) #return the read value
    queue.enqueue((0,tNo,variable)) #no unlocked values to read, enqueue the transaction

def write(tNo,variable,value,sites,queue):
    allAlive = findAlive(variable,sites) #find all sites with variable
    for siteIndex in allAlive:
        #print sites[siteIndex].exLocks[variable]
        #print tNo
        if (-1 != sites[siteIndex].exLocks[variable] and tNo != sites[siteIndex].exLocks[variable]) or sites[siteIndex].sharedLocks[variable] != []: #check if the transaction doesn't hold the exLock or any other lock exists
            #print "QUEUEING"
            queue.enqueue((1,tNo,variable))
            return -1
    for siteIndex in allAlive: #this means we can obtain all the locks
        #print "WRITING"
        sites[siteIndex].exLocks[variable] = tNo
        sites[siteIndex].vals[variable] = value
    return 1
