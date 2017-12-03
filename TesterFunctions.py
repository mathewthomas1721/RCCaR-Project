def dump(sites,variables):
    if variable == -1:
        if len(sites) != 1:
            for i in range(1,11):
                print "SITE : " + str(i)
                print "VARIABLES STORED : " + str(sites[i].vars)
                print "VARIABLE VALUES : " + str(sites[i].vals)

        else:
            print "SITE : " + str(sites[0].index)
            print "VARIABLES STORED : " + str(sites[0].vars)
            print "VARIABLE VALUES : " + str(sites[0].vals)

    else:
        if len(sites) != 1:
            for i in range(1,11):
                print "SITE : " + str(i)
                print "VARIABLE x" + str(variable) + " VALUE : " + str(sites[i].vals[variable])
        else :
            print "SITE : " + str(sites[0].index)
            print "VARIABLE x" + str(variable) + " VALUE : " + str(sites[0].vals[variable])

def fail(siteIndex, sites):
    for site in sites:
        if site.index = siteIndex:
            site.alive = -1
            for item in site.exLocks:
                site.exLocks[i] = -1
            for item in site.sharedLocks:
                site.sharedLocks[i] = []
            break

def recover(siteIndex, sites, variables,queue):
    
