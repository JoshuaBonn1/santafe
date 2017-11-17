# world.py

import numpy as np
import random
from colorama import init, Fore, Back, Style
init()

class World:
    def __init__(self, size=1, trail=None):
        if trail == 'SantaFe':
            self.grid = np.zeros((32, 32))
            self.shape = (32, 32)
            self._loadFromFile('trail_santafe.txt')
        elif trail is not None:
            self.grid = np.zeros((32, 32))
            self.shape = (32, 32)
            self._loadFromFile(trail)
        else:
            self.grid = np.zeros((size, size))
            self.shape = (size, size)
            self.generateRandom()
        
    def __getitem__(self, vals):
        if vals == 'shape':
            return self.shape
        assert isinstance(vals, tuple), "Must be a tuple"
        assert len(vals) == 2, "Must pass two values"
        return self.grid[vals[0]][vals[1]]
    
    def __setitem__(self, vals, item):
        assert isinstance(vals, tuple), "Must be a tuple"
        assert len(vals) == 2, "Must pass two values"
        self.grid[vals[0]][vals[1]] = item
    
    def _loadFromFile(self, file):
        f = open(file, 'r')
        for r, line in enumerate(f.readlines()):
            for c, value in enumerate(line):
                if value == '\n':
                    continue
                self.grid[c][r] = int(value)
    
    def generateRandom(self):
        for x in xrange(self.shape[0]):
            for y in xrange(self.shape[1]):
                self.grid[x][y] = random.choice((0,1))
    
    def resetWorld(self):
        for x in xrange(self.grid.shape[0]):
            for y in xrange(self.grid.shape[1]):
                if self.grid[x][y] == 2 or self.grid[x][y] == 1:
                    self.grid[x][y] = 1
                else:
                    self.grid[x][y] = 0
    
    def foodCount(self):
        return np.count_nonzero(self.grid)
    
    def __str__(self):
        grid = ""
        for y in xrange(self.grid.shape[1]):
            for x in xrange(self.grid.shape[0]):
                if int(self.grid[x][y]) == 0:
                    grid += Fore.WHITE + ' ' + Fore.RESET
                elif int(self.grid[x][y]) == 1:
                    grid += Fore.GREEN + Style.BRIGHT + '+' + Fore.RESET + Style.RESET_ALL
                elif int(self.grid[x][y]) == 2:
                    grid += Fore.RED + Style.BRIGHT + '@' + Fore.RESET + Style.RESET_ALL
                elif int(self.grid[x][y]) == 3:
                    grid += Fore.WHITE + '.' + Fore.RESET
                elif int(self.grid[x][y]) == 4:
                    grid += Back.WHITE + 'A' + Back.RESET
                grid += ' '
            grid += "\n"
        return grid