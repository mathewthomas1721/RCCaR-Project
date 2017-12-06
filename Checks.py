'''
Replicated Concurrency Control and Recovery Project
Advanced Datbase Systems - Prof. Dennis Shasha

MATHEW THOMAS
N15690387
'''
'''
findAlive(variable,sites)

Finds all alive sites at which "variable" is present.

Output : Returns list of alive locations where variable is present.
'''
def findAlive(variable,sites):
    availList = []
    for site in sites:
        if site.alive == 1:
            if variable in site.vars :
                availList.append(site.index)
        elif site.alive == 0:
            if variable in site.nonReplicatedVars:
                    availList.append(site.index)
    #print "Sites With the variable : " + str(availList)
    return availList
'''
checkLocked(variable,site)

Checks if a variable at a particular site is locked or not.

Output : Returns tuple of the following format - (lockCode, listOfLocks)
lockCode is 1 if variable is exlusive locked, 0 if variable is only share locked,
and -1 if no locks are held.
listOfLocks is a list of relevant locks on the variable at that site.
'''
def checkLocked(variable,site):
    #print "\ncheckLocked called on " + str(variable) + " at site " + str(site.index)
    xclusive = site.exLocks[variable]
    shared = site.sharedLocks[variable]
    if xclusive != -1:
        return (1,[xclusive])
    elif shared != []:
        return (0,shared)
    else:
        return (-1,[-1])
