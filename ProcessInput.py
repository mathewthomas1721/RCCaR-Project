'''
Replicated Concurrency Control and Recovery Project
Advanced Datbase Systems - Prof. Dennis Shasha

MATHEW THOMAS
N15690387
'''
from Checks import findAlive
'''
read(transaction,variable,sites,queue)

Attempts to read a particular variable from any alive site. If no replica
of the variable is alive or if all replicas are locked, the transactions
waits, ie, is put in a waiting queue.

Output : Returns a tuple of the form (val,location)
If a read is successful, val will be the returned value, and location will
be the site from which the value is read.
If a read is unsuccessful, val will be -1, and location will be -1
'''
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

'''
recoverRead(variable,sites)

Attempts to read a particular variable from any alive site in order to
perform a synchronizing write upon site recovery.
If no replica of the variable is alive or if all replicas are exclusive locked,
the  recovery waits, ie, is put in a recovery queue.

Output : Returns a tuple of the form (val,location)
If a read is successful, val will be the returned value, and location will
be the site from which the value is read.
If a read is unsuccessful, val will be -1, and location will be -1
'''

def recoverRead(variable,sites):
    allAlive = findAlive(variable,sites) #find all sites with variable

    for siteIndex in allAlive:
        siteIndex = siteIndex - 1
        if -1 == sites[siteIndex].exLocks[variable] : #check if the transaction has an exLock
            return (sites[siteIndex].vals[variable], siteIndex) #return the read value
    return(-1,-1)

'''
write(transaction,variable,value,sites,queue)

Attempts to write a value to all replicas of a particular variable.
If any replica is locked, the transaction must wait (as per the available
copies algorithm).

Output : Returns an integer
If a write is successful, 1 is returned
If a write is unsuccessful, -1 is returned
'''

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

'''
recoverWrite(variable,value,site)

Performs a synchronizing write for site recovery, to be used in tandem
with recoverRead.

Output : Returns an integer
If a write is successful, 1 is returned

'''

def recoverWrite(variable,value,site):

    site.vals[variable] = value

    return 1
