from VariableClasses import Variable
from SiteClasses import Site
from ProcessInput import read, write
from TransactionScheduling import Queue
from Checks import findAlive, checkLocked

variables = []
variables.append(-1)
for i in range(1,21):
    variables.append(Variable(i,10))
sites = []
for i in range(10):
    sites.append(Site(i+1,20,variables))

#TEST THE VARIABLES AND SITES
queue = Queue()

for i in range(1,21):
    print "\nVARIABLE : " + str(i)
    print "VARIABLE VALUE : " + str(variables[i].val)
    print "VARIABLE LOCATIONS : " + str(variables[i].locs)

for i in range(10):
    print "\nSITE : " + str(sites[i].index)
    print " REPLICATED VARIABLES STORED : " + str(sites[i].replicatedVars)
    print " NON - REPLICATED VARIABLES STORED : " + str(sites[i].nonReplicatedVars)
    '''print "VARIABLE VALUES : " + str(sites[i].vals)
    print "EX LOCKS : " + str(sites[i].exLocks)
    print "SHARED LOCKS : " + str(sites[i].sharedLocks)'''

'''
print(read(1,1,sites,queue))
'''
'''
write(1,1,1,sites,queue)
positions = findAlive(1,sites)
print "SITE : VALUE"
for i in positions:
    print str(i) + ":" + str(sites[i].vals[1])
'''
'''
for i in range (1,21):
    print findAlive(i,sites)
'''
#print sites[1]
'''
print checkLocked(1,sites[1])
'''
