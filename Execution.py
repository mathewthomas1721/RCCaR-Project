'''
Replicated Concurrency Control and Recovery Project
Advanced Datbase Systems - Prof. Dennis Shasha

MATHEW THOMAS
N15690387
'''
import sys
from ReadInput import readInput
from VariableClasses import Variable
from SiteClasses import Site
from ProcessInput import read, write
from TransactionScheduling import Queue
from Checks import findAlive, checkLocked
from TransactionClasses import Transaction
from TesterFunctions import dump, fail, recover

filename = sys.argv[1]
verbose = 0
if len(sys.argv) > 2:
    if sys.argv[2] == "--verbose":
        verbose = 1

def removeDup(seq): #removes duplicates in a list, preserves order of list
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

#Initializes Database
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
f = open(filename)

for line in f.readlines():
    print "---------------------------------------------------------------------------------"
    waitingTransactions = []
    for item in queue.items:
        waitingTransactions.append(item[1])
    waitingTransactions = list(set(waitingTransactions))
    tick = tick+1
    print "TICK : " + str(tick)
    recoveryQueue = list(set(recoveryQueue))
    tempRecovery = []
    for item in recoveryQueue: #Attempts to recover sites in the recovery queue
        recoveryStatus = recover(item, sites, variables)
        if recoveryStatus != 1:
            tempRecovery.append(item)
    recoveryQueue = list(tempRecovery)

    queue.items = removeDup(queue.items)

    if queue.size()>1: #Deadlock Check
        cycles = queue.deadlock(sites)
        while len(cycles) != 0:
            if verbose == 1:
                print "\nDeadlock Detected!"
            cycle = cycles[0]
            cycle = list(set(cycle))
            deadlockedTransactions = []
            for item in cycle:
                deadlockedTransactions.append(transactions[item])
            if verbose == 1:
                print "\nBreaking Deadlock..."
            toAbort = queue.breakDeadlock(deadlockedTransactions)
            abortedTransactions.append(toAbort)
            abortedTransactions = list(set(abortedTransactions))
            print "ABORTING T" + str(toAbort)
            transactions[toAbort].endTransaction(tick,sites) #Aborts youngest transaction in deadlock
            abortedTransactions.append(toAbort)

            for inQueue in queue.items: #Removes any operations from the aborted transaction from the waiting queue
                if inQueue[1] == toAbort:
                    queue.items.remove(inQueue)
            #break
            cycles = queue.deadlock(sites)

    if queue.size()>0: #Attempting to run waiting transactions

        size = queue.size()
        i = 0
        while not queue.isEmpty() and i<size:
            i = i+1
            op = queue.dequeue()
            if op[0] == 0:
                res = read(transactions[op[1]],op[2],sites,queue)
                if res[1] == -1:
                    if verbose == 1:
                        print "\nRead Failed : T" + str(op[1])
                    queue.enqueue(op)
                else:
                    if verbose == 1:
                        print "\nRead Successful!"
                    print "\nTransaction : T" + str(op[1])+ "\nVariable : x" + str(op[2]) + "\nValue : " + str(res[0]) + "\nSite : " + str(res[1])
            elif op[0] == 1:
                res = write(transactions[op[1]],op[2],op[3],sites,queue)
                if res == -1:
                    if verbose == 1:
                        print "\nWrite Failed : T" + str(op[1])
                    queue.enqueue(op)
                else :
                    if verbose == 1:
                        print "\nWrite Successful! \nT" + str(op[1]) + "\nVariable : x" + str(op[2]) + "\nValue : " + str(op[3])

            elif op[0] == 2:
                stillWaiting = 0
                for item in queue.items:
                    if item[1] == op[1]:
                        stillWaiting = 1
                        break
                if stillWaiting == 1:
                    queue.enqueue(op)
                else:
                    if verbose == 1:
                        print("Ending Transaction " + str(op[1])+ "\n")
                    transactions[op[1]].commit(tick,sites)

    waitingTransactions = []
    for item in queue.items:
        waitingTransactions.append(item[1])
    waitingTransactions = list(set(waitingTransactions))

    print("\n"+line) #Execute the next operation in the operation list
    op = readInput(line)

    #print waitingTransactions
    if op[0] in [2,3,7] and op[1] in abortedTransactions: #Checks if the operation is part of an aborted transaction
        if verbose == 1:
            print "Operation Skipped, Transaction has been aborted"
    elif op[0] in [2,3,7] and op[1] in waitingTransactions: #Checks if the operation is part of a waiting transaction
        if op[0] == 2:
            queue.enqueue((0,op[1],op[2]))
        elif op[0] == 3:
            queue.enqueue((1,op[1],op[2],op[3]))
        else :
            queue.enqueue((2,op[1]))

        if verbose == 1:
            print "\nOperation Skipped, Transaction is Waiting"

    elif op[0] == 0 :
        if verbose == 1:
            print("\nTransaction Creation Started")
        transactions[op[1]] = Transaction(op[1],tick)


    elif op[0] == 1:
        if verbose == 1:
            print("\nRO Transaction Creation Started")
        transactions[op[1]] = Transaction(op[1],tick)
        transactions[op[1]].RO = 1
        for i in range (10):
            for var in sites[i].vals:
                if var not in transactions[op[1]].ReadValues:
                    transactions[op[1]].ReadValues[var] = (sites[i].vals[var],i+1)


    elif op[0] == 2:
        if transactions[op[1]].RO == 1:
            if verbose == 1:
                print "\nRead Successful!"
            print "\nTransaction : T" + str(op[1])+ "\nVariable : x" + str(op[2]) + "\nValue : " + str(transactions[op[1]].ReadValues[op[2]][0]) + "\nSite : " + str(transactions[op[1]].ReadValues[op[2]][1])
        else:
            res = read(transactions[op[1]],op[2],sites,queue)

            if res[0] != -1:
                if verbose == 1:
                    print "\nRead Successful!"
                print "\nTransaction : T" + str(op[1])+ "\nVariable : x" + str(op[2]) + "\nValue : " + str(res[0]) + "\nSite : " + str(res[1])
            else :
                if verbose == 1:
                    print "\nCouldn't Read x" + str(op[2]) + ", T" + str(op[1]) + " must wait"

    elif op[0] == 3:
        res = write(transactions[op[1]],op[2],op[3],sites,queue)
        if res == 1:
            if verbose == 1:
                print "\nWrite Successful! \nT" + str(op[1]) + "\nVariable : x" + str(op[2]) + "\nValue : " + str(op[3])
        elif res == -1:
            if verbose == 1:
                print "Couldn't Write x" + str(op[2]) + ", T" + str(op[1]) + " must wait"



    elif op[0] == 4:
        if verbose == 1:
            print("\nDump of all variables started\n")
        dump(sites,-1)

    elif op[0] == 5:
        if verbose == 1:
            print("\nDump of all variables at site " + str(op[1])+" started\n")
        dump([sites[op[1]-1]],-1)

    elif op[0] == 6:
        if verbose == 1:
            print("\nDump of variable x" + str(op[1]) + " at all sites started\n")
        dump(sites,op[1])

    elif op[0] == 7:
        if verbose == 1:
            print("\nEnding Transaction " + str(op[1])+ "\n")
        transactions[op[1]].commit(tick,sites)


    elif op[0] == 8:
        if verbose == 1:
            print("\nFailing Site " + str(op[1]) + "\n")
        resAborted = fail(op[1], sites,transactions,tick)
        abortedTransactions = abortedTransactions + resAborted
        abortedTransactions = list(set(abortedTransactions))

    elif op[0] == 9:
        if verbose == 1:
            print("\nRecovering Site " + str(op[1]))
        recoveryStatus = recover(op[1], sites, variables)
        if recoveryStatus == -1:
            if verbose == 1:
                print "Can't recover yet, will try in subsequent ticks"
            recoveryQueue.append(op[1])

keepRunning = 0
while not (queue.isEmpty() or len(recoveryQueue) != 0) and keepRunning<=500 : #Continues running waiting transactions/site recoveries after all operations have been received
    keepRunning = keepRunning + 1
    print "---------------------------------------------------------------------------------"
    tick = tick+1
    print "TICK : " + str(tick)

    recoveryQueue = list(set(recoveryQueue))
    tempRecovery = []
    for item in recoveryQueue:
        recoveryStatus = recover(item, sites, variables)
        if recoveryStatus != 1:
            tempRecovery.append(item)

    recoveryQueue = list(tempRecovery)

    queue.items = removeDup(queue.items)
    if queue.size()>1:
        cycles = queue.deadlock(sites)
        while len(cycles) != 0:
            if verbose == 1:
                print "\nDeadlock Detected!"
            cycle = cycles[0]
            cycle = list(set(cycle))
            deadlockedTransactions = []
            for item in cycle:
                deadlockedTransactions.append(transactions[item])
            if verbose == 1:
                print "\nBreaking Deadlock..."
            toAbort = queue.breakDeadlock(deadlockedTransactions)
            abortedTransactions.append(toAbort)
            abortedTransactions = list(set(abortedTransactions))
            print "\nABORTING T" + str(toAbort)
            transactions[toAbort].endTransaction(tick,sites)

            for inQueue in queue.items:
                if inQueue[1] == toAbort:
                    queue.items.remove(inQueue)
            cycles = queue.deadlock(sites)

    if queue.size()>0:
        size = queue.size()
        i = 0
        while not queue.isEmpty() and i<size:
            i = i+1
            op = queue.dequeue()
            if op[0] == 0:
                res = read(transactions[op[1]],op[2],sites,queue)
                if res[1] == -1:
                    if verbose == 1:
                        print "\nRead Failed : T" + str(op[1])
                    queue.enqueue(op)
                else:
                    print "\nTransaction : T" + str(op[1])+ "\nVariable : x" + str(op[2]) + "\nValue : " + str(res[0]) + "\nSite : " + str(res[1])
            elif op[0] == 1:
                res = write(transactions[op[1]],op[2],op[3],sites,queue)
                if res == -1:
                    if verbose == 1:
                        print "\nWrite Failed : T" + str(op[1])
                    queue.enqueue(op)
                else :
                    if verbose == 1:
                        print "\nWrite Successful! \nT" + str(op[1]) + "\nVariable : x" + str(op[2]) + "\nValue : " + str(op[3])
            elif op[0] == 2:
                stillWaiting = 0
                for item in queue.items:
                    if item[1] == op[1]:
                        stillWaiting = 1
                        break
                if stillWaiting == 1:
                    queue.enqueue(op)
                else:
                    print("\nEnding Transaction " + str(op[1])+ "\n")
                    transactions[op[1]].commit(tick,sites)
            
if keepRunning>500:
    if verbose == 1:
        print("\nUNABLE TO COMPLETE TRANSACTIONS IN WAITING QUEUE AFTER 500 TICKS!\nABORTING TRANSACTIONS IN WAITING QUEUE!\n")

        for item in queue.items:
            print "ABORTING T" + str(item[1])
            transactions[item[1]].endTransaction(tick,sites) #Aborts youngest transaction in deadlock
            abortedTransactions.append(item[1])
            for inQueue in queue.items: #Removes any operations from the aborted transaction from the waiting queue
                if inQueue[1] == item[1]:
                    queue.items.remove(inQueue)
