# generation.py

import ant
from copy import deepcopy
import random
import matplotlib.pyplot as plt

class Generation:
    def __init__(self, size, elite, mutate, tournament, steps):
        self.size = size
        self.elite = elite
        self.mutate = mutate
        self.tournament = tournament
        self.steps = steps
        self.cleanup = True
        self._createGeneration()
        self.bests = []
        self.avgs = []
    
    def _createGeneration(self):
        self.ants = []
        for _ in xrange(self.size):
            self.ants.append(ant.Ant())
    
    def run(self, worlds, generations):
        #Run for n generations
        for gen in xrange(generations):
            world = random.choice(worlds)
            world_max = world.foodCount()
            #Simulated all ants
            for ant in self.ants:
                ant.fitness = 0
                if self.cleanup:
                    ant.program.cleanUp()
                ant.run(world, self.steps)
                world.resetWorld()
                ant.reset()
                ant.fitness = ant.fitness / float(world_max)
            
            
            self.best = max(self.ants, key=lambda x: x.fitness)
            self.bests.append(self.best.fitness)
            self.avgs.append(float(sum([a.fitness for a in self.ants])) / float(len(self.ants)))
            print 'Generation:', gen, '; Food Collected:', self.bests[-1], ';', self.avgs[-1]
            
            if gen == generations - 1:
                break
            #Do not change top elite
            elite = int(self.elite * len(self.ants))
            self.ants = sorted(self.ants, key=lambda a: a.fitness, reverse=True)
            new_ants = []
            for ant in xrange(elite):
                new_ants.append(deepcopy(self.ants[ant]))
            
            #Perform selection and mutation
            target_length = len(self.ants)
            while True:
                child1, child2 = self.crossover()
                child1.mutateSelf(self.mutate)
                child2.mutateSelf(self.mutate);
                if len(new_ants) < target_length:
                    new_ants.append(child1)
                else:
                    break
                if len(new_ants) < target_length:
                    new_ants.append(child2)
                else:
                    break
            
            self.ants = new_ants
    
    def printFitnesses(self):
        for i, ant in enumerate(self.ants):
            print 'Individual ' + str(i) + ': ' + str(ant.fitness)
    
    def selection(self):
        #Tournament Selection
        try:
            selection = random.sample(self.ants, self.tournament)
        except ValueError:
            selection = self.ants
        return max(selection, key=lambda x: x.fitness)
    
    def crossover(self):
        child1 = deepcopy(self.selection())
        child2 = deepcopy(self.selection())
        child1.crossover(child2)
        return child1, child2
    
    def showGraph(self):
        avgs, = plt.plot(range(0, len(self.avgs)), self.avgs, 'b-', label='Average')
        bests, = plt.plot(range(0, len(self.bests)), self.bests, 'g-', label='Best')
        plt.legend(handles=[avgs, bests])
        plt.xlabel('Generations')
        plt.ylabel('Food Collected')
        plt.title('Genetic Programming for Santa Fe Trail')
        plt.show()
    
    def __str__(self):
        r = 'Generation Info:' + '\n'
        r += '\tPopulation Size: ' + str(self.size) + '\n'
        r += '\tMutation Rate: ' + str(self.mutate) + '\n'
        r += '\tElite Percentage: ' + str(self.elite) + '\n'
        r += '\tTournament Size: ' + str(self.tournament) + '\n'
        r += '\tNumber of Steps: ' + str(self.steps) + '\n'
        return r