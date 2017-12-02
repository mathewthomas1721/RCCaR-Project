def findAlive(variable,sites):
    availList = []
    for site in sites:
        if site.alive == 1:
            if variable in site.vars :
                availList.append(site.index)
    return availList

def checkLocked(variable,site):
    xclusive = site.exLocks[variable]
    shared = site.sharedLocks[variable]
    if xclusive != -1:
        return (1,[xclusive])
    elif shared != []:
        return (0,shared)
    else:
        return (-1,[-1])
