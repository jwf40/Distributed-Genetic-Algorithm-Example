import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class Agent(object):
    """
    Agents of the population
    The basic unit of the simulation
    """
    def __init__(self,target_score):
        """
        Constructor
            |genotype: Numeric representation of attributes, list, dtype=int
            |colour: an RGB representation of the fitness. Each channel represents fitness in the respective dimension. list, dtype=int
            |fitness: numeric value to represent the strength of an individual
            |target: target score to evolve
        """
        self.genotype = []
        self.colour = []
        self.fitness = None
        self.target = target_score

    def __str__(self):
        """
        Information to be printed out
        """
        return str("Gentoype: " + str(self.genotype) + " Fitness: " + str(self.fitness) + " Colour: " + str(self.colour))

    def init_genotype(self):
        """
        Randomly initialise the genotype of the individual
        """
        for i in range(3):
            self.genotype.append(np.random.randint(400))

    def calc_fitness(self):
        """
        Arguments:
            |target: Desired resultant values
        Returns:
            |fitness score
        calculates absolute distance of current solution from desired outcome. Sums in all dimensions.
        """
        assert len(self.target) == len(self.genotype)
        fitness = 0
        for i in range(len(self.genotype)):
            fitness += abs(self.genotype[i] - self.target[i])
        self.fitness = fitness
        return fitness

    def calc_colour(self):
        """
        calculates the colour to represent the solution.
        Brighter indicates stronger solutions
        Specific colour indicates fitness in certain dimensions
        """
        self.colour = []
        for i in range(len(self.genotype)):
            self.colour.append((self.target[i] - self.genotype[i]) % 255)

    def replace(self, winner,mutation_rate):#
        """
        Arguments:
            |winner: strongest individual of the last epoch population
            |mutation_rate: likelihood of mutation occuring.
        Replaces loser with a copy of the winner, then has a chance to evolve in any/all dimensions
        """
        self.genotype = winner
        for i in self.genotype:
            if mutation_rate >= np.random.randint(0, 10):
                i = np.random.randint(400)
        self.calc_colour()

target_score = [20,35,120] #Desired result
population = np.empty(2500, dtype=Agent) #Instantiate numpy array
mut_rate = 2 #mutation rate
for i in range(len(population)):
    #Instantiate population
    population[i] = Agent(target_score)
    population[i].init_genotype()
    population[i].calc_colour()
    population[i].calc_fitness()

population = np.reshape(population, (50, 50)) #Make 2D, for image representation
timestep = 0
max_epoch = 2500
while(timestep < max_epoch):
    for _ in range(20):
        winner = (np.random.randint(len(population[0])), np.random.randint(len(population[1])))
        #25, 40, 20
        left = 0
        right = 50
        top = 0
        bottom = 50
        neighbourhood_size = 5
        #Agents belong to neighbourhoods.
        if (winner[0] - neighbourhood_size) > left:
            left = winner[0] - neighbourhood_size
        if (winner[0] + neighbourhood_size) <= right:
            right = winner[0] + neighbourhood_size
        if (winner[1] - neighbourhood_size) > top:
            top = winner[1] - neighbourhood_size
        if (winner[1] + neighbourhood_size) <= bottom:
            bottom = winner[1] + neighbourhood_size
        neighbourhood = population[left:right, top:bottom]
        loser  = (np.random.randint(left, right), (np.random.randint(top, bottom)))

        #Tournament selection
        if population[winner[0]][winner[1]].fitness > population[loser[0]][loser[1]].fitness:
            temp = winner
            winner = loser
            loser = winner
        population[loser[0]][loser[1]].replace(population[winner[0]][winner[1]].genotype,mut_rate)
        population[loser[0]][loser[1]].calc_fitness()
        population[loser[0]][loser[1]].calc_colour()
        #Find best solutions and print out
        neighbourhood_1d = np.reshape(neighbourhood, np.prod(neighbourhood.shape))
        neighbourhood_1d = sorted(neighbourhood_1d[:1], key=lambda x:x.fitness)
        for w in neighbourhood_1d:
            print("Winners of Timestep: " + str(timestep) + "\n" + str(w))
    #Parse data and save to PNG file.
    col_pop = np.empty((50,50, 3), dtype=np.uint8)
    for i in range(len(population[0])):
        for j in range(len(population[1])):
            for k in range(3):
                col_pop[i][j][k] = (population[i][j].colour[k])
    col_pop = np.asarray(col_pop)
    if (timestep % 100 == 0) or timestep == max_epoch-1:
        img = Image.fromarray(col_pop)
        img.save('rgb' + str(timestep) + '.png')
    timestep += 1
#Find winners.
pop = np.reshape(population, 2500)
winners = sorted(pop, key=lambda x:x.fitness)
winners = winners[:2]
for w in winners:
    print("Winners of RUN: " + str(timestep) + str(w))
