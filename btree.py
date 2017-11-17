def getMaxDepth(l):
    max_node = max(l, key=lambda x: x[1])[1]
    depth = 0
    prior = 0
    while 2**depth + prior < max_node:
        prior += 2**depth
        depth += 1
    return depth

def findVal(l, n):
    for v, i in l:
        if i == n:
            return str(v)
    return '|'

def _printTree(l, depth, vals=0, currval=0):
    if depth != 0:
        for i in xrange(currval, 2**vals + currval):
            line = ""
            line += ' '*(2**(depth - 1) - 1)
            line += '_'*(2**(depth - 1))
            line += findVal(l, i)
            line += '_'*(2**(depth - 1))
            line += ' '*(2**(depth - 1) - 1)
            print line,
            currval+=1
        print ''
        _printTree(l, depth - 1, vals+1, currval)
    else:
        for i in xrange(currval, 2**vals + currval):
            print findVal(l, i),
        print ''
        
def printTree(l):
    _printTree(l, getMaxDepth(l))

# l = []
# l.append(('P',0))
# l.append(('I',1))
# l.append(('P',2))
# l.append(('I',3))
# l.append(('I',4))
# l.append(('F',5))
# l.append(('F',6))
# l.append(('L',7))
# l.append(('F',8))
# l.append(('R',9))
# l.append(('F',10))

# printTree(l)