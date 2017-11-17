# amt.py

import random
from copy import deepcopy

class Node:
    debug = False

    def __init__(self, parent=None):
        self.op = None
        self.action = None
        self.left = None
        self.right = None  
        self.parent = parent
    
    def generateTree(self, depth):
        #if at first node, generate internal node
        self.op = random.choice(internal_nodes)
        self.left = Node()
        self.left._generateTree(depth - 1, self)
        self.right = Node()
        self.right._generateTree(depth - 1, self)
    
    def _generateTree(self, depth, p):
        self.parent = p
        if depth == 0:
            #Only leaf, base case
            self.op = random.choice(leaf_nodes)
            self.action = random.choice(actions)
        else:
            #Recursive case
            self.op = random.choice(internal_nodes + leaf_nodes)#[item for sublist in [internal_nodes, leaf_nodes] for item in sublist])
            if self.op in leaf_nodes:
                self.action = random.choice(actions)
            else:
                self.left = Node()
                self.left._generateTree(depth - 1, self)
                self.right = Node()
                self.right._generateTree(depth - 1, self)
    
    def runTree(self, ant, world):
        #if self.debug:
        #    print self.op.__name__
        self.op(self, ant, world)
    
    def doLeft(self, ant, world):
        if self.left is None:
            print "DEAD LEAF"
        else:
            self.left.runTree(ant, world)

    def doRight(self, ant, world):
        if self.right is None:
            print "DEAD LEAF"
        else:
            self.right.runTree(ant, world)
        
    def Prog2(self, ant, world):
        if self.debug:
            print 'Prog2'
        self.doLeft(ant, world)
        self.doRight(ant, world)

    def If(self, ant, world):
        if self.debug:
            print 'If1'
        #Check if ant position + direction is food
        new_location = self._wrapAround(ant.location + ant.getMovement(), world['shape'])
        if world[tuple(new_location)] == 1:
            self.doLeft(ant, world)
        else:
            self.doRight(ant, world)

    def Leaf(self, ant, world):
        if self.debug:
            print self.action.__name__
        self.action(ant)
        
    def _wrapAround(self, pos, shape):
        if 0 > pos[0]:
            pos[0] = int(shape[0]) - 1
        elif pos[0] >= shape[0]:
            pos[0] = 0
        elif 0 > pos[1]:
            pos[1] = int(shape[1]) - 1
        elif pos[1] >= shape[1]:
            pos[1] = 0
        return pos 
    
    def mutateSelf(self, rate):
        # Mutate self--only between node types?
        if self.left is None and self.right is None:
            if rate > random.random():
                self.action = random.choice(actions)
        else:
            if rate > random.random():
                self.op = random.choice(internal_nodes)
            self.right.mutateSelf(rate)
            self.left.mutateSelf(rate)
    
    def getRandomNode(self):
        choice = None
        try:
            count, choice = self.left._getRandomNode(-1, self)
            count, choice = self.right._getRandomNode(count, choice)
        except:
            print self.action, self.left, self.right
        if choice == self:
            assert False, "Crossing over root node"
        return choice
    
    def _getRandomNode(self, count, choice):
        if self.left is None and self.right is None:
            # Base case
            if count == -1:
                return count+1, self
            elif random.randint(0, count + 1) == count:
                return count+1, self
            else:
                return count+1, choice
        else:
            # Recursive Case
            if self.left is None:
                assert True, 'Bad internal node, Left'
            if self.right is None:
                assert True, 'Bad internal node, Right'
            count, choice = self.left._getRandomNode(count, choice)
            count, choice = self.right._getRandomNode(count, choice)
            if random.randint(0, count + 1) == count:
                return count+1, self
            else:
                return count+1, choice
    
    def swap(self, other):
        parent1 = self.parent
        parent2 = other.parent
        if self == parent1.left:
            parent1.left = other
        else:
            parent1.right = other
        other.parent = parent1
        if other == parent2.left:
            parent2.left = self
        else:
            parent2.right = self
        self.parent = parent2
    
    def cleanUp(self, food=None):
        if self.left is None and self.right is None:
            return
        if self.op == Node.If:
            self.left.cleanUp(True)
            self.right.cleanUp(False)
        else:
            self.left.cleanUp(food)
            self.right.cleanUp(food)
        # Checks if the left side of an if node is an if
        if self.left.left is not None:
            if self.op == Node.If and self.left.op == Node.If:
                self.left = self.left.left
        # Checks if the right side of an if node is an if
        if self.right.right is not None:
            if self.op == Node.If and self.right.op == Node.If:
                self.right = self.right.right
        # Checks if both cases of an if statement are the same
        if self.left.action == self.right.action and self.left.action is not None and self.op == Node.If and self.left.op == Node.Leaf:
            self.op = Node.Leaf
            self.action = deepcopy(self.left.action)
            self.left = None
            self.right = None
                    
    def prune(self, depth):
        #check left and right concerning depth. If depth is hit, set self as leaf and set left and right as none
        if depth == 0:
            self.left = None
            self.right = None
            self.op = Node.Leaf
            self.action = random.choice(actions)
        elif self.left is None and self.right is None:
            pass
        else:
            self.left.prune(depth-1)
            self.right.prune(depth-1)
    
    def count(self):
        return self._count()
    
    def _count(self):
        c = 0
        if self.right is not None:
            c += self.right._count()
        if self.left is not None:
            c += self.left._count()
        return c + 1
        
    def rPrint(self, d):
        if self.left is None and self.right is None:
            if self.action is None:
                print '\t'*d + 'NOPE'
            else:
                print '\t'*d + self.action.__name__
        else:
            self.right.rPrint(d+1)
            print '\t'*d + self.op.__name__
            self.left.rPrint(d+1)
    
    def __str__(self):
        self.rPrint(0)
        return 'Done'

def turnLeft(ant):
    #print "Turning Left"
    ant.move('L')
    
def turnRight(ant):
    #print "Turning Right"
    ant.move('R')
    
def moveForward(ant):
    #print "Moving Forward"
    ant.move('F')

internal_nodes = (Node.If, Node.Prog2)
leaf_nodes = (Node.Leaf,)
actions = (turnLeft, turnRight, moveForward)