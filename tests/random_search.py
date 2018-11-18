import numpy as np

class RandomSearch:
    def __init__(self, gene_set):
        self.gene_set = gene_set
        self.best_fitness = -np.inf

    def randomChromossome(self, rankingSize):
        return np.random.choice(self.gene_set, size=rankingSize, replace=False)

    def initializePopulation(self, chromosomeSize = 100, populationSize = 100):
        self.population_size = populationSize
        self.chromosome_size = chromosomeSize
        population = []
        for i in range(populationSize):            
            population.append(self.randomChromossome(chromosomeSize))
        self.population = population

    def step(self, fitness_function):
        fitness_values = [fitness_function(individual) for individual in self.population]
        current_best = np.max(fitness_values)
        if current_best > self.best_fitness:
            self.best_fitness = current_best
        new_population = []
        for i in range(self.population_size):            
            new_population += [self.randomChromossome(self.chromosome_size)]
        self.population = new_population