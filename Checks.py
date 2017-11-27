findAlive(variable,sites):
    availList = []
    for site in sites:
        if site.alive = 1:
            if variable in site.vars :
                availList.append(site.index)
    return availList

checkLocked(variable,site):
    xclusive = site.exLocks[variable]
    shared = site.sharedLocks[variable]
    if xclusive != -1:
        return [xclusive]
    elif shared != []
        return shared
    else
        return [-1]
