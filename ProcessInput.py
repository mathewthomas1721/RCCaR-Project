from Checks import findAlive
def read(transaction,variable,sites,queue):

    allAlive = findAlive(variable,sites) #find all sites with variable
    for siteIndex in allAlive:
        if transaction.tNo == sites[siteIndex].exLocks[variable] or -1 == sites[siteIndex].exLocks[variable] : #check if the transaction has an exLock or there isn't an exLock
            sites[siteIndex].sharedLocks[variable].append(transaction.tNo) #add this transaction to shared locks
            if siteIndex not in transaction.sharedLocks:
                transaction.sharedLocks[siteIndex] = variable
            else :
                transaction.sharedLocks[siteIndex].append(variable)
            return (sites[siteIndex].vals[variable], siteIndex) #return the read value
    queue.enqueue((0,transaction.tNo,variable)) #no unlocked values to read, enqueue the transaction
    return(-1,-1)

def recoverRead(variable,sites):
    allAlive = findAlive(variable,sites) #find all sites with variable
    for siteIndex in allAlive:
        if -1 == sites[siteIndex].exLocks[variable] : #check if the transaction has an exLock
            return (sites[siteIndex].vals[variable], siteIndex) #return the read value
    return(-1,-1)

def write(transaction,variable,value,sites,queue):

    allAlive = findAlive(variable,sites) #find all sites with variable
    for siteIndex in allAlive:
        #print sites[siteIndex].exLocks[variable]
        #print tNo
        if (-1 != sites[siteIndex].exLocks[variable] and transaction.tNo != sites[siteIndex].exLocks[variable]) or sites[siteIndex].sharedLocks[variable] != []: #check if the transaction doesn't hold the exLock or any other lock exists
            #print "QUEUEING"
            queue.enqueue((1,transaction.tNo,variable))
            return -1
    for siteIndex in allAlive: #this means we can obtain all the locks
        #print "WRITING"
        if siteIndex not in transaction.exLocks:
            transaction.sharedLocks[siteIndex] = variable
        else :
            transaction.exLocks[siteIndex].append(variable)
        sites[siteIndex].exLocks[variable] = transaction.tNo
        sites[siteIndex].vals[variable] = value
    return 1

def recoverWrite(variable,value,site):

    site.vals[variable] = value
    
    return 1
