from Checks import findAlive
def read(transaction,variable,sites,queue):
    #print("READING")
    allAlive = findAlive(variable,sites) #find all sites with variable
    for siteIndex in allAlive:
        siteIndex = siteIndex - 1
        if transaction.tNo == sites[siteIndex].exLocks[variable] or -1 == sites[siteIndex].exLocks[variable] : #check if the transaction has an exLock or there isn't an exLock
            sites[siteIndex].sharedLocks[variable].append(transaction.tNo) #add this transaction to shared locks
            #print sites[siteIndex].index, sites[siteIndex].sharedLocks
            if siteIndex+1 not in transaction.sharedLocks:
                transaction.sharedLocks[siteIndex+1] = [variable]
            else :
                transaction.sharedLocks[siteIndex+1].append(variable)
            return (sites[siteIndex].vals[variable], siteIndex+1) #return the read value
    queue.enqueue((0,transaction.tNo,variable)) #no unlocked values to read, enqueue the transaction
    return(-1,-1)

def recoverRead(variable,sites):
    #print("READING TO RECOVER")
    allAlive = findAlive(variable,sites) #find all sites with variable
    for siteIndex in allAlive:
        siteIndex = siteIndex - 1
        if -1 == sites[siteIndex].exLocks[variable] : #check if the transaction has an exLock
            return (sites[siteIndex].vals[variable], siteIndex) #return the read value
    return(-1,-1)

def write(transaction,variable,value,sites,queue):
    #print("WRITING")
    allAlive = findAlive(variable,sites) #find all sites with variable
    for siteIndex in allAlive:
        siteIndex = siteIndex-1
        #print sites[siteIndex].exLocks[variable]
        #print tNo
        if (-1 != sites[siteIndex].exLocks[variable] and transaction.tNo != sites[siteIndex].exLocks[variable]) or (sites[siteIndex].sharedLocks[variable] != [] and sites[siteIndex].sharedLocks[variable] != [transaction.tNo]): #check if the transaction doesn't hold the exLock or any other lock exists
            #print "QUEUEING"
            queue.enqueue((1,transaction.tNo,variable,value))
            return -1
    for siteIndex in allAlive: #this means we can obtain all the locks
        #print "WRITING"
        siteIndex = siteIndex-1
        if siteIndex+1 not in transaction.exLocks:
            transaction.exLocks[siteIndex+1] = [variable]
        else :
            transaction.exLocks[siteIndex+1].append(variable)
        sites[siteIndex].exLocks[variable] = transaction.tNo
        #Commenting out direct write, wait for commit instead
        #sites[siteIndex].vals[variable] = value
        transaction.opList.append((variable,siteIndex+1,value))
    return 1

def recoverWrite(variable,value,site):
    #print("WRITING RECOVERED VALUES")

    site.vals[variable] = value

    return 1
