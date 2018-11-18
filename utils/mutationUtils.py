import numpy as np

def generateMutant(gene_set, chromosome):
    possibilidades = list(gene_set)
    if(chromosome.__len__() < possibilidades.__len__()):
        while True:
            mutant = np.random.choice(possibilidades)
            if(not chromosome.__contains__(mutant)):
                return mutant
            else:
                possibilidades.remove(mutant)
    else:
        return None