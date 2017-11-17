# ant.py

import node

_debug = False

class Position:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def __getitem__(self, i):
        if i == 0:
            return self.a
        elif i == 1:
            return self.b
    
    def __setitem__(self, i, val):
        if i == 0:
            self.a = val
        elif i == 1:
            self.b = val
    
    def __iter__(self):
        yield self.a
        yield self.b
    
    def __add__(self, other):
        assert isinstance(other, Position), "Other must be a Position"
        return Position(self[0] + other[0], self[1] + other[1])
    
    def __str__(self):
        return str(tuple(self))

directions = {"N": Position(0, -1), 
              "E": Position(1, 0), 
              "S": Position(0, 1), 
              "W": Position(-1, 0)}

class Ant:
    total_steps = 0

    def __init__(self, depth=5):
        self.location = Position(0, 0)
        self.direction = "E"
        self.program = node.Node()
        self.program.generateTree(depth)
        self.world = None
        self.fitness = 0
    
    def mutateSelf(self, rate):
        self.program.mutateSelf(rate)
    
    def crossover(self, other):
        #Get two random nodes, swap all important values
        if self.count() == 1 or other.count() == 1:
            return
        subtree1 = self.program.getRandomNode()
        subtree2 = other.program.getRandomNode()
        subtree1.swap(subtree2)
        self.program.prune(10)
        other.program.prune(10)
    
    def getMovement(self):
        return directions[self.direction]
    
    #@profile
    def run(self, world, steps, show_bot=False):
        self.total_steps = steps
        self.fitness = 0
        self.world = world
        if self.world[tuple(self.location)] == 1:
            self.world[tuple(self.location)] = 2
            self.fitness += 1
        else:
            self.world[tuple(self.location)] = 3
        for _ in xrange(steps):
            if self.total_steps == 0:
                break
            self.program.runTree(self, world)
        if show_bot:
            self.world[tuple(self.location)] = 4
    
    def count(self):
        return self.program.count()
    
    def move(self, action):
        #Move forward or turn
        if action == 'F':
            self.goForward()
        else:
            self.turn(action)
    
    def turn(self, direction):
        #Turn left or right
        if direction == 'R':
            self.turnRight()
        elif direction == 'L':
            self.turnLeft()
        else:
            assert True, str(direction) + "is not a allowed direction."
    
    def turnRight(self):
        if self.total_steps != 0:
            dirs = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
            if _debug:
                print "Turning right from " + self.direction + " to " + dirs[self.direction]
            self.direction = dirs[self.direction]
            self.total_steps -= 1
    
    def turnLeft(self):
        if self.total_steps != 0:
            dirs = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
            if _debug:
                print "Turning left from " + self.direction + " to " + dirs[self.direction]
            self.direction = dirs[self.direction]
            self.total_steps -= 1
    
    def goForward(self):
        if self.total_steps != 0:
            #Move forward and wrap around world
            if _debug:
                print "Moving from " + str(self.location) + " to",
            self.location += directions[self.direction]
            if 0 > self.location[0]:
                self.location[0] = int(self.world['shape'][0]) - 1
            elif self.location[0] >= self.world['shape'][0]:
                self.location[0] = 0
            elif 0 > self.location[1]:
                self.location[1] = int(self.world['shape'][1]) - 1
            elif self.location[1] >= self.world['shape'][1]:
                self.location[1] = 0
            if self.world[tuple(self.location)] == 1.0:
                self.world[tuple(self.location)] = 2
                self.fitness += 1
            elif self.world[tuple(self.location)] == 0.0:
                self.world[tuple(self.location)] = 3
            if _debug:
                print str(self.location)
            self.total_steps -= 1
    
    def reset(self):
        self.location = Position(0, 0)
        self.direction = "E"
    
    def __str__(self):
        return 'Ant at ' + str(self.location) + ' facing ' + self.direction + '; Fitness: ' + str(self.fitness)

            