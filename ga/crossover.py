import numpy as np
from utils.mutationUtils import generateMutant


class Crossover:
    def __init__(self , kind= 1):
        self.kind = kind

    def setup(self, gene_set, chromosomeSize):
        self.chromosomeSize = chromosomeSize
        self.gene_set = gene_set

    def __call__(self, chromosome1, chromosome2):
        kind = self.kind
        if(kind == 1):
            return self.crossoverMoreMutants(chromosome1, chromosome2)
        elif(kind == 2):
            return self.crossoverLessMutants(chromosome1, chromosome2)
        else:
            return None

    # crossover com maior variação, se um gene de um cromossomo se repete deve ocorrer uma mutação o que pode 
    # provocar uma variação desmedida (tendo em vista o numero elevado de genes possiveis) o que me faz temer
    # a não convergência da população
    def crossoverMoreMutants(self, chromosome1, chromosome2):
        newChromosome1 = []
        newChromosome2 = []
        for i in range(self.chromosomeSize):
            gene = np.random.choice([chromosome1[i],chromosome2[i]])
            if gene == chromosome1[i] :
                geneComplementar = chromosome2[i]
            else:
                geneComplementar = chromosome1[i]
            if newChromosome1.count(gene)==1 : 
                newChromosome1 += [generateMutant(self.gene_set, newChromosome1)]
            else:    
                newChromosome1 += [gene]
            if newChromosome2.count(geneComplementar)==1 : 
                newChromosome2 += [generateMutant(self.gene_set, newChromosome2)]
            else:    
                newChromosome2 += [geneComplementar]
        return [newChromosome1, newChromosome2]

    # crossover com menos variação entre os filhos, mais apropiado para convergência
    def crossoverLessMutants(self, chromosome1, chromosome2):
        newChromosome1 = []
        newChromosome2 = []
        for i in range(self.chromosomeSize):
            gene = np.random.choice([chromosome1[i],chromosome2[i]])
            if gene == chromosome1[i] :
                geneComplementar = chromosome2[i]
            else:
                geneComplementar = chromosome1[i]
            if newChromosome1.count(gene)==1 :
                newElement = np.random.choice(np.random.choice([chromosome1,chromosome2]))
                while newChromosome1.__contains__(newElement):
                    newElement = np.random.choice(np.random.choice([chromosome1,chromosome2])) 
                newChromosome1 += [newElement]
            else:    
                newChromosome1 += [gene]
            if newChromosome2.count(geneComplementar)==1 :
                newElement = np.random.choice(np.random.choice([chromosome1,chromosome2])) 
                while newChromosome2.__contains__(newElement):
                    newElement = np.random.choice(np.random.choice([chromosome1,chromosome2])) 
                newChromosome2 += [newElement]
            else:    
                newChromosome2 += [geneComplementar]
        return [newChromosome1, newChromosome2]
