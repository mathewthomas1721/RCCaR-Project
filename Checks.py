findAlive(variable,sites):
    availList = []
    for site in sites:
        if variable in site.vars:
            availList.append(site.index)
    return availList

checkLocked(variable,site):
    xclusive = site.locks[variable]
    shared = site.sharedLocks[variable]
    if xclusive != -1:
        return [xclusive]
    elif shared != []
        return shared
    else
        return -1
