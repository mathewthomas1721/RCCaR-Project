# Replicated-Concurrency-Control-and-Recovery-Project

## Functions

### Read Input
#### readInput(inputString)
Reads in each line of input Returns list of operations


### Process Input
#### read(transaction,variable,sites,queue)
Attempts to read a particular variable from any alive site. If no replica
of the variable is alive or if all replicas are locked, the transactions
waits, ie, is put in a waiting queue.

Output : Returns a tuple of the form (val,location)
If a read is successful, val will be the returned value, and location will
be the site from which the value is read.
If a read is unsuccessful, val will be -1, and location will be -1
#### write(transaction,variable,value,sites,queue)
Attempts to write a value to all replicas of a particular variable.
If any replica is locked, the transaction must wait (as per the available
copies algorithm).

Output : Returns an integer
If a write is successful, 1 is returned
If a write is unsuccessful, -1 is returned

####recoverRead(variable,sites)
Attempts to read a particular variable from any alive site in order to
perform a synchronizing write upon site recovery.
If no replica of the variable is alive or if all replicas are exclusive locked, the  recovery waits, ie, is put in a recovery queue.

Output : Returns a tuple of the form (val,location)
If a read is successful, val will be the returned value, and location will
be the site from which the value is read.
If a read is unsuccessful, val will be -1, and location will be -1

####recoverWrite(variable,value,site)
Performs a synchronizing write for site recovery, to be used in tandem
with recoverRead.

Output : Returns an integer
If a write is successful, 1 is returned

### Checks for Input Processing
#### findAlive(variable,sites)
Finds all alive sites at which "variable" is present.

Output : Returns list of alive locations where variable is present.
#### checkLocked(variable,site)
Checks if a variable at a particular site is locked or not.

Output : Returns tuple of the following format - (lockCode, listOfLocks)
lockCode is 1 if variable is exlusive locked, 0 if variable is only share locked,
and -1 if no locks are held.
listOfLocks is a list of relevant locks on the variable at that site.

### Transaction Scheduling
#### class Queue
A simple queue implementation to simulate a waiting queues for
transactions/operations that are forced to wait.

items : all operations in the waiting queue. Operations are in the form
of tuples :

(0,tNo,variable)) -> Corresponds to a read operation from a transaction "tNo"
for "variable"

(1,transaction.tNo,variable,value) -> Corresponds to a write operation from
a transaction "tNo" for writing "value" to "variable"

(2,tNo) -> Corresponds to an end() for a transaction "tNo"

####isEmpty()
Checks whether the waiting queue is empty

Output : Returns True if empty, False if not

####enqueue(item)
Adds an item to the waiting queue

####dequeue()
Pops an item from the waiting queue

Output : returns the popped item

####size()
Finds the length of the waiting queue

Output : Returns the length of the waiting queue
####dfsCycleCheck(graph, start, end)
Checks if there is a cycle in a path from "start" to "end" in "graph"

Output : Returns any cycle in the path from "start" to "end"
#### deadlock(self,sites)
Checks for any deadlocks in the waiting queue

Output : Returns a list of any cycles present in the graph
#### breakDeadlock(transactions)
Returns the youngest transaction in the deadlock cycle, which will be terminated
to break the deadlock

Output : Returns tNo of the youngest transaction in the deadlock cycle


### Tester Functions
#### dump(sites,variable)
Displays variable values based on parameters.

dump(sites, -1) - Displays all variable values for all sites
dump([site],-1) - Displays all variable values at a particular site
dump(sites, variable)  - Displays all values for a particular variable at
all sites
dump([site], variable) - Diplays value of variable at a particular site
#### fail(siteIndex, sites,transactions,tick)
Fails a specific site, essentially simulating a server failure.

Output : Returns a list of transactions that are aborted as a result of
the failure
#### recover(siteIndex, sites, variables)
Recovers a previously failed site

Output : Returns 1 if the site has all variables available for access
Returns -1 if only non-replicated data is available for access
