# Replicated-Concurrency-Control-and-Recovery-Project

## Functions

### Read Input
#### readInput(inputString)
Reads in each line of input Returns list of operations
### Process Input
#### read(tNo, variable)
Finds all copies of variable that are available (at alive sites)
Checks which copies are not locked.
Prints value from one of the unlocked available sites and the site from which the value was read. If all copies are locked, it waits.
#### write(tNo,variable,value)
Finds all copies of variable that are available (at alive sites). Checks which copies are not locked.
If any copies are locked, it waits.
Writes value to all available sites.
### Checks for Input Processing
#### findAlive(variable)
Finds all sites where copies of a variable are available. Returns a list of those sites.
#### checkLocked(variable,site)
Checks whether a variable is locked at a particular site. Returns Boolean value.
### Transaction Scheduling
#### enqueue(transaction,variable,sites)
Enqueues a transaction if it needs to wait. Keeps track of the variable(s) it is waiting for.
#### deadlock(queue)
Checks for deadlock periodically. Returns Boolean.
#### breakDeadlock(queue)
Finds the youngest transaction in a deadlock and aborts it.
### Tester Functions
#### dump(sites = all, variable = all)
Gives the committed values of all copies of all variables at all sites, sorted per site.
If a particular site is passed as argument, all committed variable values at a particular site are displayed.
If a particular variable is passed as argument, all committed values for that variable at all sites are displayed.
By default, all copies of all variables at all sites are displayed, sorted per site.
#### fail(site)
Simulates a site failing, ie, marks that site as failed. This marks variable replicas at that site as unavailable.
#### recover(site)
Simulates site recovery.
Makes non-replicated data instantly available.
Does not make replicated data available until a synchronizing committed write is completed.
