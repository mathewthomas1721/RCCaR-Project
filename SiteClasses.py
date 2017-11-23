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

class Site:

    def __init__(self, index, numVar,varVals):
        self.index = index
        self.vars = []
        self.vals = {}
        

        for i in range(1,numVar+1):
            if (1 + (i%10)) == index:
                self.vars.append(i)
                self.vals[i] = varVals[i].val
            elif i%2 == 0:
                self.vars.append(i)
                self.vals[i] = varVals[i].val
        self.exclusiveLock = []
        self.sharedLock = Queue();
