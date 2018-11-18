import numpy as np
from utils.mutationUtils import generateMutant

class Mutation:
    def __init__(self, mutation_rate=0.01):
        self.mutation_rate = mutation_rate

    def setup(self, gene_set):
        self.gene_set = gene_set

    def __call__(self, chromosome):
        mutationGenes = []   
        newChromossome = chromosome 
        chromosomeSize = chromosome.__len__()
        places = [a for a in range(chromosome.__len__())]
        numberOfMutations = int(chromosomeSize*self.mutation_rate)
        for i in range(numberOfMutations):
            while True:
                place = np.random.choice(places)
                if(not chromosome.__contains__(place)):
                    mutationGenes += [place]
                    break
                else:
                    places.remove(place)                                                                                                                                    
        for place in mutationGenes:
            mutant = generateMutant(self.gene_set, newChromossome)   
            newChromossome[place] = mutant
        return newChromossome