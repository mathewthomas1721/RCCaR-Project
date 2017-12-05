from Checks import findAlive, checkLocked

'''
class Queue

A simple queue implementation to simulate a waiting queues for
transactions/operations that are forced to wait.

items : all operations in the waiting queue. Operations are in the form
of tuples :

(0,tNo,variable)) -> Corresponds to a read operation from a transaction "tNo"
for "variable"

(1,transaction.tNo,variable,value) -> Corresponds to a write operation from
a transaction "tNo" for writing "value" to "variable"

(2,tNo) -> Corresponds to an end() for a transaction "tNo"

'''

'''
isEmpty()

Checks whether the waiting queue is empty

Output : Returns True if empty, False if not
'''

'''
enqueue(item)

Adds an item to the waiting queue
'''

'''
dequeue()

Pops an item from the waiting queue

Output : returns the popped item
'''

'''
size()

Finds the length of the waiting queue

Output : Returns the length of the waiting queue

'''

'''
dfsCycleCheck(graph, start, end)

Checks if there is a cycle in a path from "start" to "end" in "graph"

Output : Returns any cycle in the path from "start" to "end"

'''

'''
deadlock(self,sites)

Checks for any deadlocks in the waiting queue

Output : Returns a list of any cycles present in the graph
'''

'''
breakDeadlock(transactions)

Returns the youngest transaction in the deadlock cycle, which will be terminated
to break the deadlock

Output : Returns tNo of the youngest transaction in the deadlock cycle
'''
class Queue:
    def __init__(self):
        self.items = []


    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)



    def dequeue(self):
        return self.items.pop()



    def size(self):
        return len(self.items)



    def dfsCycleCheck(self, graph, start, end):
        #print("\nCHECKING FOR CYCLES\n")
        #print graph
        fringe = [(start, [])]
        while fringe:
            state, path = fringe.pop()
            if path and state == end:
                yield path
                continue
            #print graph[state]
            for next_state in graph[state]:
                if next_state in path:
                    continue
                fringe.append((next_state, path+[next_state]))



    def deadlock(self,sites):
        #print("\nCHECKING FOR DEADLOCK\n")
        #print self.items
        requirementsGraph = {}
        for item in self.items:
            rw = item[0]

            if rw != 2:
                variable = item[2]
                locations = findAlive(variable,sites)
                reqs = []
                for loc in locations :
                    locks = checkLocked(variable,sites[loc-1])
                    if locks[0] != -1: #no locks on this variable
                        if rw == 1: #all locks for a write operation
                            reqs = reqs + locks[1]
                        elif locks[0] == 1 : #only write locks for read operations
                            reqs = reqs + locks[1]

                requirementsGraph[item[1]] = list(set(reqs)) #all the transactions that are blocking each transaction in the queue
        endNodes = []
        for node in requirementsGraph:
            for item in requirementsGraph[node]:
                if item not in requirementsGraph:
                    endNodes.append(item)
        for node in endNodes:
            requirementsGraph[node] = []
        #print requirementsGraph
        cycles = [[node]+path  for node in requirementsGraph for path in self.dfsCycleCheck(requirementsGraph, node, node)]
        for cycle in cycles:
            if len(set(cycle)) <= 1:
                cycles.remove(cycle)
        #print cycles
        return cycles

    def breakDeadlock(self,transactions):
        #print("\nBREAKING DEADLOCK\n")
        minTrans = -1
        maxStart = 0
        for transaction in transactions :
            if transaction.startTime>maxStart:
                minTrans = transaction.tNo
                maxStart = transaction.startTime
        self.items = [x for x in self.items if x[1] != minTrans]
        return minTrans
