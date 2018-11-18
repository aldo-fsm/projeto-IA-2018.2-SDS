import numpy as np
from ga import GeneticAlgorithm, Crossover, Mutation, Selection
from matplotlib import pyplot as plt

def testWithFakeFitness(table_len=1000, pop_size=100, chr_size=10, generations_to_run=200):
    fake_fitness_table = np.random.randn(table_len)
    def fake_fitness_function(chromossome):
        return np.mean(fake_fitness_table[chromossome])
    gene_set = list(range(table_len))
    selection = Selection(0.5)
    crossover = Crossover()
    mutation = Mutation(0.01)
    optimizer = GeneticAlgorithm(gene_set, selection, crossover, mutation)
    optimizer.initializePopulation(chr_size, pop_size)
    plt.grid()
    for i in range(generations_to_run):
        optimizer.step(fake_fitness_function)
        plt.scatter([i]*pop_size, [fake_fitness_function(x) for x in optimizer.population], c='b')
    plt.show()