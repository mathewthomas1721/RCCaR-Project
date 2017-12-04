import sys
from ReadInput import readInput
from VariableClasses import Variable
from SiteClasses import Site
from ProcessInput import read, write
from TransactionScheduling import Queue
from Checks import findAlive, checkLocked
from TransactionClasses import Transaction
from TesterFunctions import dump, fail, recover

variables = []
variables.append(-1)
for i in range(1,21):
    variables.append(Variable(i,10))
sites = []
for i in range(1,11):
    sites.append(Site(i,20,variables))


queue = Queue()
tick = 0
transactions = {}
recoveryQueue = []

print("\nDefault Variable Values and Sites Created\n")
for line in sys.stdin:
    print line
    tick = tick+1
    for item in recoveryQueue:
        print("\nAttempting Recovery on items in Recovery Queue\n")
        recoveryStatus = recover(item, sites, variables)
        if recoveryStatus == -1:
            print "Can't recover yet, will try in subsequent ticks"
            recoveryQueue.append(op[1])

    op = readInput(line)
    print op

    '''
    begin(Tn) -> (0,n)
    beginRO(Tn) -> (1,n)
    R(Tn,xm) -> (2,n,m)
    W(Tn,xm,v) -> (3,n,m,v)
    dump() -> (4)
    dump(i) -> (5,i)
    dump(xj) -> (6,j)
    end(Tn) -> (7,n)
    fail(n) -> (8,n)
    recover(n) -> (9,n)
    '''
    if op[0] == 0 :
        print("\nTransaction Creation Started\n")
        transactions[op[1]] = Transaction(op[1],tick)

    elif op[0] == 1:
        print("\nRO Transaction Creation Started\n")
        transactions[op[1]] = Transaction(op[1],tick)

    elif op[0] == 2:
        print("\nRead Started\n")
        res = read(transactions[op[1]],op[2],sites,queue)
        if res[0] != -1:
            print "\nVariable : x" + str(op[2]) + "\nValue : " + str(res[0]) + "\nSite : " + str(res[1])
        else :
            print "\nCouldn't Read x" + str(op[2]) + ", T" + str(op[1]) + " must wait"

    elif op[0] == 3:
        print("\nWrite Started\n")
        res = write(transactions[op[1]],op[2],op[3],sites,queue)
        if res == 1:
            print "\n Write Successful! \nT" + str(op[1]) + "\nVariable : x" + str(op[2]) + "\nValue : " + str(op[3])
        elif res == -1:
            print "\nCouldn't Write x" + str(op[2]) + ", T" + str(op[1]) + " must wait"

    elif op[0] == 4:
        print("\nDump all variables started\n")
        dump(sites,-1)

    elif op[0] == 5:
        print("\nDump all variables at site " + str(op[1])+" started\n")
        dump([sites[op[1]-1]],-1)

    elif op[0] == 6:
        print("\nDump variable x" + str(op[1]) + " at all sites started\n")
        dump(sites,op[1])

    elif op[0] == 7:
        print("\nEnding Transaction " + str(op[1])+ "\n")
        transaction = transactions[op[1]]
        transaction.endTransaction(tick,sites)


    elif op[0] == 8:
        print("\nFailing Site " + str(op[1]) + "\n")
        fail(op[1], sites)

    elif op[0] == 9:
        print("\nRecovering Site " + str(op[1]) + "\n")
        recoveryStatus = recover(op[1], sites, variables)
        if recoveryStatus == -1:
            print "Can't recover yet, will try in subsequent ticks"
            recoveryQueue.append(op[1])
