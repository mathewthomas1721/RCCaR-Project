from Checks import findAlive
read(tNo,variable,sites,queue):
    allAlive = findAlive(variable,sites)
    for siteIndex in allAlive:
        if variable not in sites[siteIndex].exLocks:
            sites[siteIndex].sharedLocks[variable].append(tNo)
            return sites[siteIndex].vals[variable], siteIndex
    queue.enqueue((0,tNo,variable))

write(tNo,variable,value,sites,queue):
    allAlive = findAlive(variable,sites)
    for siteIndex in allAlive:
        if variable in sites[siteIndex].exLocks or variable in sites[siteIndex].sharedLocks:
            queue.enqueue((1,tNo,variable))
            return -1
    for siteIndex in allAlive:
        sites[siteIndex].exLocks[variable] = tNo
        sites[siteIndex].vals[variable] = value
    return 1
