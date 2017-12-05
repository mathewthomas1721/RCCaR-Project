'''
readInput(inputString)

Reads input line by line from the file and translates it for processing.

Output : A variable length tuple is returned. Each type of instruction
corresponds to a particular tuple type as shown below.

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

def readInput(inputString):
    inputString = inputString.replace(", ", ",")
    #print inputString
    inputString = inputString.rstrip().split()
    ops = []
    for item in inputString:
        if 'begin(' in item:
            item = int(item[7:len(item)-1])
            tup = (0,item)
        elif 'beginRO(' in item:
            item = int(item[9:len(item)-1])
            tup = (1,item)
        elif 'R(' in item:
            item = item[3:len(item)-1]
            item = item.split(',')
            tup = (2,int(item[0]),int(item[1][1:]))
        elif 'W(' in item:
            item = item[3:len(item)-1]
            item = item.split(',')
            tup = (3,int(item[0]),int(item[1][1:]),int(item[2]))
        elif 'dump()' in item:
            tup = (4,-1)
        elif 'dump(x' in item:
            tup = (6,int(item[6:len(item)-1]))
        elif 'dump(' in item:
            item = item[5:len(item)-1]
            tup = (5,int(item))
        elif 'end(' in item:
            item = item[5:len(item)-1]
            tup = (7,int(item))
        elif 'fail(' in item:
            item = item[5:len(item)-1]
            tup = (8,int(item))
        elif 'recover(' in item:
            item = item[8:len(item)-1]
            tup = (9,int(item))
        else :
            print "INVALID OPERATION : " + item


    return tup
