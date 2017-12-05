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
abortedTransactions = []
waitingTransactions = []

#print("\nTick = " + str(tick) + " Default Variable Values and Sites Created")
for line in sys.stdin:
    print "---------------------------------------------------------------------------------"
    waitingTransactions = []
    for item in queue.items:
        waitingTransactions.append(item[1])
    waitingTransactions = list(set(waitingTransactions))
    tick = tick+1
    #print "RECOVERY QUEUE"
    #print recoveryQueue
    recoveryQueue = list(set(recoveryQueue))
    tempRecovery = []
    for item in recoveryQueue:
        #print("Tick = " + str(tick) + " Attempting Recovery on item in Recovery Queue" + str(item))
        recoveryStatus = recover(item, sites, variables)
        if recoveryStatus != 1:
            #print "Can't recover yet, will try in subsequent ticks"
            tempRecovery.append(item)

    recoveryQueue = list(tempRecovery)
    queue.items = list(set(queue.items))
    #print queue.items
    if queue.size()>1:
        #print queue.size()
        #print("\nTick = " + str(tick) + " WAITING QUEUE : " + str(queue.items))
        cycles = queue.deadlock(sites)
        while len(cycles) != 0:
            cycle = cycles[0]
            cycle = list(set(cycle))
            deadlockedTransactions = []
            for item in cycle:
                deadlockedTransactions.append(transactions[item])

            toAbort = queue.breakDeadlock(deadlockedTransactions)
            abortedTransactions.append(toAbort)
            abortedTransactions = list(set(abortedTransactions))
            print "ABORTING T" + str(toAbort)
            transactions[toAbort].endTransaction(tick,sites)
            abortedTransactions.append(toAbort)
            #print "REMOVING ABORTED TRANSACTION T" + str(toAbort)
            for inQueue in queue.items:
                if inQueue[1] == toAbort:
                    queue.items.remove(inQueue)
            #print "REMOVED ABORTED TRANSACTION T" + str(toAbort)
            #print "UPDATED WAITING QUEUE : "   + str(queue.items)
            break
            cycles = queue.deadlock(sites)
    #print queue.items
    if queue.size()>0:
        #print "EXECUTING WAITING TRANSACTIONS"
        size = queue.size()
        i = 0
        while not queue.isEmpty() and i<size:
            #print queue.items
            i = i+1
            op = queue.dequeue()
            print op
            if op[0] == 0:
                res = read(transactions[op[1]],op[2],sites,queue)
                if res[1] == -1:
                    queue.enqueue(op)
                else:
                    print "\nVariable : x" + str(op[2]) + "\nValue : " + str(res[0]) + "\nSite : " + str(res[1])
            elif op[0] == 1:
                res = write(transactions[op[1]],op[2],op[3],sites,queue)
                if res == -1:
                    queue.enqueue(op)
                else :
                    print "\nWrite Successful! \nT" + str(op[1]) + "\nVariable : x" + str(op[2]) + "\nValue : " + str(op[3])

            elif op[0] == 2:
                print("Tick = " + str(tick) + " Ending Transaction " + str(op[1])+ "\n")
                transactions[op[1]].commit(tick,sites)
    waitingTransactions = []
    for item in queue.items:
        waitingTransactions.append(item[1])
    waitingTransactions = list(set(waitingTransactions))
    print("\nTick = " + str(tick) + " " + line)
    op = readInput(line)
    #print("Tick = " + str(tick) + " Operation Read : " + str(op))

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
    '''print "ABORTED TRANSACTIONS"
    print abortedTransactions'''
    if op[0] in [2,3,7] and op[1] in abortedTransactions:
        print "Tick = " + str(tick) + " Operation Skipped, Transaction already aborted"
    elif op[0] in [2,3,7] and op[1] in waitingTransactions:
        if op[0] == 2:
            queue.enqueue((0,op[1],op[2]))
        elif op[0] == 3:
            queue.enqueue((1,op[1],op[2],op[3]))
        else :
            queue.enqueue((2,op[1]))

        print "Tick = " + str(tick) + " Operation Skipped, Transaction waiting"

    elif op[0] == 0 :
        print("Tick = " + str(tick) + " Transaction Creation Started")
        transactions[op[1]] = Transaction(op[1],tick)


    elif op[0] == 1:
        print("Tick = " + str(tick) + " RO Transaction Creation Started")
        transactions[op[1]] = Transaction(op[1],tick)
        transactions[op[1]].RO = 1
        for i in range (10):
            for var in sites[i].vals:
                if var not in transactions[op[1]].ReadValues:
                    transactions[op[1]].ReadValues[var] = (sites[i].vals[var],i+1)
        #print transactions[op[1]].ReadValues

    elif op[0] == 2:
        #print("Tick = " + str(tick) + " Read Started : x" + str(op[2]))
        if transactions[op[1]].RO == 1:
            print "\nVariable : x" + str(op[2]) + "\nValue : " + str(transactions[op[1]].ReadValues[op[2]][0]) + "\nSite : " + str(transactions[op[1]].ReadValues[op[2]][1])
        else:
            res = read(transactions[op[1]],op[2],sites,queue)

            if res[0] != -1:
                print "\nVariable : x" + str(op[2]) + "\nValue : " + str(res[0]) + "\nSite : " + str(res[1])
            else :
                print "\nCouldn't Read x" + str(op[2]) + ", T" + str(op[1]) + " must wait"
                #waitingTransactions.append(op[1])
    elif op[0] == 3:
        #print("\nTick = " + str(tick) + " Write Started : x" + str(op[2]) + " with value " + str(op[3]))
        res = write(transactions[op[1]],op[2],op[3],sites,queue)
        if res == 1:
            print "\nWrite Successful! \nT" + str(op[1]) + "\nVariable : x" + str(op[2]) + "\nValue : " + str(op[3])
        elif res == -1:
            print "Couldn't Write x" + str(op[2]) + ", T" + str(op[1]) + " must wait"
            #waitingTransactions.append(op[1])

    elif op[0] == 4:
        print("Tick = " + str(tick) + " Dump all variables started\n")
        dump(sites,-1)

    elif op[0] == 5:
        print("Tick = " + str(tick) + " Dump all variables at site " + str(op[1])+" started\n")
        dump([sites[op[1]-1]],-1)

    elif op[0] == 6:
        print("Tick = " + str(tick) + " Dump variable x" + str(op[1]) + " at all sites started\n")
        dump(sites,op[1])

    elif op[0] == 7:
        print("Tick = " + str(tick) + " Ending Transaction " + str(op[1])+ "\n")
        transactions[op[1]].commit(tick,sites)


    elif op[0] == 8:
        print("Tick = " + str(tick) + " Failing Site " + str(op[1]) + "\n")
        resAborted = fail(op[1], sites,transactions,tick)
        abortedTransactions = abortedTransactions + resAborted
        abortedTransactions = list(set(abortedTransactions))

    elif op[0] == 9:
        print("Tick = " + str(tick) + " Recovering Site " + str(op[1]) + "\n")
        recoveryStatus = recover(op[1], sites, variables)
        if recoveryStatus == -1:
            print "Can't recover yet, will try in subsequent ticks"
            recoveryQueue.append(op[1])
    '''for site in sites:
        print site.index, site.sharedLocks'''


while not queue.isEmpty or len(recoveryQueue) != 0:

    #print "RECOVERY QUEUE"
    #print recoveryQueue
    recoveryQueue = list(set(recoveryQueue))
    tempRecovery = []
    for item in recoveryQueue:
        #print("Tick = " + str(tick) + " Attempting Recovery on item in Recovery Queue" + str(item))
        recoveryStatus = recover(item, sites, variables)
        if recoveryStatus != 1:
            #print "Can't recover yet, will try in subsequent ticks"
            tempRecovery.append(item)

    recoveryQueue = list(tempRecovery)

    queue.items = list(set(queue.items))
    if queue.size()>1:
        #print queue.size()
        #print("\nTick = " + str(tick) + " WAITING QUEUE : " + str(queue.items))
        cycles = queue.deadlock(sites)
        while len(cycles) != 0:
            cycle = cycles[0]
            cycle = list(set(cycle))
            deadlockedTransactions = []
            for item in cycle:
                deadlockedTransactions.append(transactions[item])

            toAbort = queue.breakDeadlock(deadlockedTransactions)
            abortedTransactions.append(toAbort)
            abortedTransactions = list(set(abortedTransactions))
            print "ABORTING T" + str(toAbort)
            transactions[toAbort].endTransaction(tick,sites)

            #print "REMOVING ABORTED TRANSACTION T" + str(toAbort)
            for inQueue in queue.items:
                if inQueue[1] == toAbort:
                    queue.items.remove(inQueue)
            #print "REMOVED ABORTED TRANSACTION T" + str(toAbort)
            #print "UPDATED WAITING QUEUE : "   + str(queue.items)
            break
            cycles = queue.deadlock(sites)

    if queue.size()>0:
        #print "EXECUTING WAITING TRANSACTIONS"
        size = queue.size()
        i = 0
        while not queue.isEmpty() and i<size:
            print queue.items
            i = i+1
            op = queue.dequeue()
            if op[0] == 0:
                res = read(transactions[op[1]],op[2],sites,queue)
                if res[1] == -1:
                    queue.enqueue(op)
                else:
                    print "\nVariable : x" + str(op[2]) + "\nValue : " + str(res[0]) + "\nSite : " + str(res[1])
            elif op[0] == 1:
                res = write(transactions[op[1]],op[2],op[3],sites,queue)
                if res == -1:
                    queue.enqueue(op)
                else :
                    print "\nWrite Successful! \nT" + str(op[1]) + "\nVariable : x" + str(op[2]) + "\nValue : " + str(op[3])
