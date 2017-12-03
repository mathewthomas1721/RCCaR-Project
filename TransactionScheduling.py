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

    def dfsCycleCheck(graph, start, end):
        fringe = [(start, [])]
        while fringe:
            state, path = fringe.pop()
            if path and state == end:
                yield path
                continue
            for next_state in graph[state]:
                if next_state in path:
                    continue
                fringe.append((next_state, path+[next_state]))

    def deadlock(self,sites):
        requirementsGraph = {}
        for item in self.items:
            rw = item[0]
            variable = item[2]
            locations = Checks.findAlive(variable,sites)
            reqs = []
            for loc in locations :
                locks = checkLocked(variable,loc)
                if locks[0] != -1: #no locks on this variable
                    if rw == 1: #all locks for a write operation
                        reqs.append(locks[1])
                    elif locks[0] == 1 : #only write locks for read operations
                        reqs.append(locks[1])
            requirementsGraph[item[1]] = reqs #all the transactions that are blocking each transaction in the queue

        cycles = [[node]+path  for node in requirementsGraph for path in dfsCycleCheck(requirementsGraph, node, node)]
        return cycles

    def breakDeadlock(self,transactions):
        minTrans = -1
        minStart = 10000000
        for transaction in transactions :
            if transaction.startTime<minStart:
                minTrans = transaction.tNo
                minStart = transaction.startTime
        self.items = [x for x in self.items if x[1] != minTrans]
        return minTrans
