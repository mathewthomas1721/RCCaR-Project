def findAlive(variable,sites):
    #print "\nfindAlive called on " + str(variable)
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
