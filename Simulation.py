from VariableClasses import Variable
from SiteClasses import Site

variables = []
variables.append(-1)
for i in range(1,21):
    variables.append(Variable(i,10))
sites = []
sites.append(-1)
for i in range(1,11):
    sites.append(Site(i,20,variables))

#TEST THE VARIABLES AND SITES

''''for i in range(1,21):
    print "VARIABLE : " + str(i)
    print "VARIABLE VALUE : " + str(variables[i].val)
    print "VARIABLE LOCATIONS : " + str(variables[i].locs)'''

for i in range(1,11):
    print "SITE : " + str(i)
    print "VARIABLES STORED : " + str(sites[i].vars)
    print "VARIABLE VALUES : " + str(sites[i].vals)
    print "CURRENT LOCKS : " + str(sites[i].locks)
