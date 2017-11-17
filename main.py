# main.py

import node
import world
import ant
import generation
from copy import deepcopy

def main():
    all_worlds = []
    simple_worlds = []
    dense_worlds = []
    moderate_worlds = []
    sparse_worlds = []
    
    for i in xrange(1, 11):
        file_name = 'trail_' + str(i) + '.txt'
        w = world.World(trail=file_name)
        all_worlds.append(w)
        simple_worlds.append(w)
    
    for i in xrange(1, 4):
        file_name = 'dense_' + str(i) + '.txt'
        w = world.World(trail=file_name)
        all_worlds.append(w)
        dense_worlds.append(w)
    
    for i in xrange(1, 4):
        file_name = 'moderate_' + str(i) + '.txt'
        w = world.World(trail=file_name)
        all_worlds.append(w)
        moderate_worlds.append(w)
    
    for i in xrange(1, 4):
        file_name = 'sparse_' + str(i) + '.txt'
        w = world.World(trail=file_name)
        all_worlds.append(w)
        sparse_worlds.append(w)
    
    
    # One test for All worlds
    all_g = generation.Generation(size=100, elite=0.1, mutate=0.15, tournament=10, steps=500)
    all_g.cleanup = True
    print all_g
    all_g.run(all_worlds, 200)
    
    # One test for simple trails
    simple_g = generation.Generation(size=100, elite=0.1, mutate=0.15, tournament=10, steps=500)
    simple_g.cleanup = True
    print simple_g
    simple_g.run(simple_worlds, 200)
    
    # One test for random worlds
    random_g = generation.Generation(size=100, elite=0.1, mutate=0.15, tournament=10, steps=500)
    random_g.cleanup = True
    print random_g
    random_g.run(dense_worlds + moderate_worlds + sparse_worlds, 200)
    
    # One test for one dense world
    dense_g = generation.Generation(size=100, elite=0.1, mutate=0.15, tournament=10, steps=500)
    dense_g.cleanup = True
    print dense_g
    dense_g.run(random.choice(dense_worlds), 200)
    
    # One test for one moderate world
    moderate_g = generation.Generation(size=100, elite=0.1, mutate=0.15, tournament=10, steps=500)
    moderate_g.cleanup = True
    print moderate_g
    moderate_g.run(random.choice(moderate_worlds), 200)
    
    # One test for one sparse world
    sparse_g = generation.Generation(size=100, elite=0.1, mutate=0.15, tournament=10, steps=500)
    sparse_g.cleanup = True
    print sparse_g
    sparse_g.run(random.choice(sparse_worlds), 200)
    
    # One test for one simple world
    simple1_g = generation.Generation(size=100, elite=0.1, mutate=0.15, tournament=10, steps=500)
    simple1_g.cleanup = True
    print simple1_g
    simple1_g.run(random.choice(simple_worlds), 200)
    
    
    # Load each test world
    simple_test = world.World(trail='SantaFe')
    dense_test = world.World(trail='dense_test.txt')
    moderate_test = world.World(trail='moderate_test.txt')
    sparse_test = world.World(trail='sparse_test.txt')
    tests = [simple_test, dense_test, moderate_test, sparse_test]
    
    bests = [all_g.best, simple_g.best, random_g.best, denst_g.best, moderate_g.best, sparse_g.best, simple1_g.best]
    # Test best from each generation on each test world
    for best in bests:
        for test in tests:
            best.run(test, 500)
            best.reset()
            test.resetWorld()
            print best.fitness / test.foodCount(), '\t'
        print '\n'


if __name__ == "__main__":
    main()