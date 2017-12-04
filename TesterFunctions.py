def dump(sites,variable):
    if variable == -1:

        if len(sites) != 1:
            print("\nDUMPING ALL VARIABLES FOR ALL SITES\n")
            for i in range(0,10):
                print "SITE : " + str(i+1)
                print "VARIABLES STORED : " + str(sites[i].vars)
                print "VARIABLE VALUES : " + str(sites[i].vals)

        else:
            print("\nDUMPING ALL VARIABLES FOR A PARTICULAR SITE\n")
            print "SITE : " + str(sites[0].index)
            print "VARIABLES STORED : " + str(sites[0].vars)
            print "VARIABLE VALUES : " + str(sites[0].vals)

    else:
        if len(sites) != 1:
            print("\nDUMPING ALL VALUES OF VARIABLE AT ALL SITES\n")
            for i in range(1,11):
                print "SITE : " + str(i)
                print "VARIABLE x" + str(variable) + " VALUE : " + str(sites[i].vals[variable])
        else :
            print("\nDUMPING VARIABLE VALUE AT PARTICULAR SITE\n")
            print "SITE : " + str(sites[0].index)
            print "VARIABLE x" + str(variable) + " VALUE : " + str(sites[0].vals[variable])

def fail(siteIndex, sites):
    print("\nFAILING A PARTICULAR SITE\n")
    for site in sites:
        if site.index == siteIndex:
            site.alive = -1
            for item in site.exLocks:
                site.exLocks[i] = -1
            for item in site.sharedLocks:
                site.sharedLocks[i] = []
            self.unavailable = list(self.replicatedVars)
            break

def recover(siteIndex, sites, variables):
    print("\nRECOVERING A PARTICULAR SITE\n")
    for site in sites:
        if site.index == siteIndex:
            for variable in site.unavailable:
                readValue = recoverRead(variable,sites)
                if readValue[1] != -1 :
                    recoverWrite(variable,value,site)
                    site.unavailable.remove(variable)

            if site.unavailable == []:
                site.alive = 1
                return 1
            else:
                site.alive = 0
                return -1
