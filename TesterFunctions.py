from ProcessInput import recoverRead, recoverWrite
def dump(sites,variable):
    if variable == -1:

        if len(sites) != 1:
            print("DUMPING ALL VARIABLES FOR ALL SITES\n")
            for i in range(0,10):
                print "\n\nSITE : " + str(i+1)
                print "VARIABLES STORED : " + str(sites[i].vars)
                print "VARIABLE VALUES : " + str(sites[i].vals)

        else:
            print("DUMPING ALL VARIABLES FOR A PARTICULAR SITE\n")
            print "\n\nSITE : " + str(sites[0].index)
            print "VARIABLES STORED : " + str(sites[0].vars)
            print "VARIABLE VALUES : " + str(sites[0].vals)

    else:
        if len(sites) != 1:
            print("DUMPING ALL VALUES OF VARIABLE AT ALL SITES\n")
            for i in range(1,11):
                print "\n\nSITE : " + str(i)
                print "VARIABLE x" + str(variable) + " VALUE : " + str(sites[i].vals[variable])
        else :
            print("DUMPING VARIABLE VALUE AT PARTICULAR SITE\n")
            print "\n\nSITE : " + str(sites[0].index)
            print "VARIABLE x" + str(variable) + " VALUE : " + str(sites[0].vals[variable])

def fail(siteIndex, sites,transactions,tick):
    print("FAILING A PARTICULAR SITE")
    aborted = []
    for site in sites:
        if site.index == siteIndex:
            site.alive = -1
            for item in site.exLocks:
                if site.exLocks[item] != -1:
                    print "ABORTING T" + str(site.exLocks[item])
                    transactions[site.exLocks[item]].endTransaction(tick,sites)
                    aborted.append(site.exLocks[item])
                site.exLocks[item] = -1

            #print "ABORTING TRANSACTIONS HOLDING READ LOCKS AT " + str(site.index)
            for item in site.sharedLocks:
                for tNo in site.sharedLocks[item]:
                    print "ABORTING T" + str(tNo)
                    transactions[tNo].endTransaction(tick,sites)
                    aborted.append(tNo)
                site.sharedLocks[item] = []
            site.unavailable = list(site.replicatedVars)


            break
    aborted = list(set(aborted))
    return aborted
def recover(siteIndex, sites, variables):
    print("RECOVERING A PARTICULAR SITE")
    for site in sites:
        if site.index == siteIndex:
            for variable in site.unavailable:
                readValue = recoverRead(variable,sites)
                if readValue[1] != -1 :
                    recoverWrite(variable,readValue[0],site)
                    site.unavailable.remove(variable)

            if site.unavailable == []:
                site.alive = 1
                print ("RECOVERED!")
                return 1
            else:
                print ("PARTIALLY RECOVERED!")
                site.alive = 0
                return -1
