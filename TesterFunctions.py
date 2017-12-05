from ProcessInput import recoverRead, recoverWrite

'''
dump(sites,variable)

Displays variable values based on parameters.

dump(sites, -1) - Displays all variable values for all sites
dump([site],-1) - Displays all variable values at a particular site
dump(sites, variable)  - Displays all values for a particular variable at
all sites
dump([site], variable) - Diplays value of variable at a particular site
'''

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

'''
fail(siteIndex, sites,transactions,tick)

Fails a specific site, essentially simulating a server failure.

Output : Returns a list of transactions that are aborted as a result of
the failure
'''

def fail(siteIndex, sites,transactions,tick):
    print("FAILING A PARTICULAR SITE")
    aborted = []
    for site in sites:
        if site.index == siteIndex:
            site.alive = -1
            for item in site.exLocks:
                if site.exLocks[item] != -1:
                    print "ABORTING T" + str(site.exLocks[item])
                    aborted.append(int(site.exLocks[item]))
                    transactions[site.exLocks[item]].endTransaction(tick,sites)
                    site.exLocks[item] = -1

            #print "ABORTING TRANSACTIONS HOLDING READ LOCKS AT " + str(site.index)
            for item in site.sharedLocks:
                for tNo in site.sharedLocks[item]:
                    print "ABORTING T" + str(tNo)
                    aborted.append(tNo)
                    transactions[tNo].endTransaction(tick,sites)

                site.sharedLocks[item] = []
            site.unavailable = list(site.replicatedVars)


            break
    aborted = list(set(aborted))
    #print aborted
    return aborted

'''
recover(siteIndex, sites, variables)

Recovers a previously failed site

Output : Returns 1 if the site has all variables available for access
Returns -1 if only non-replicated data is available for access
'''
def recover(siteIndex, sites, variables):
    print("RECOVERING SITE" + str(siteIndex))
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
