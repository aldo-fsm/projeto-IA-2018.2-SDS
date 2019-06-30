import numpy as np

class GeneticAlgorithm:
    def __init__(self, gene_set, selection_op, crossover_op, mutation_op):
        self.selection = selection_op
        self.crossover = crossover_op
        self.mutation = mutation_op
        self.gene_set = gene_set

    def randomChromossome(self, rankingSize):
        return np.random.choice(self.gene_set, size=rankingSize, replace=False)

    def initializePopulation(self, chromosomeSize = 100, populationSize = 100):
        self.mutation.setup(self.gene_set)
        self.crossover.setup(self.gene_set, chromosomeSize)
        self.population_size = populationSize
        population = []
        for i in range(populationSize):            
            population += [self.randomChromossome(chromosomeSize)]
        self.population = population

    def crossoverGenerator(self, pairs):
        for pair in pairs:
            children = self.crossover(*pair)
            for child in children:
                yield child

    def step(self, fitness_function):
        fitness_values = [fitness_function(individual) for individual in self.population]
        survivors = self.selection(self.population, fitness_values)
        if not isinstance(survivors, list):
            survivors = survivors.tolist()
        num_pairs = int(np.ceil((len(self.population) - len(survivors))/2))
        pairs = [(survivors[i], survivors[i+1]) for i in range(num_pairs)]
        new_population = survivors
        gen = self.crossoverGenerator(pairs)
        for _ in range(self.population_size - len(survivors)):
            new_population.append(self.mutation(next(gen)))
        self.population = new_population
        best_index = np.argmax(fitness_values)
        self.best_fitness = fitness_values[best_index]

#================================ GA ANTIGO ==========================================
    # def optimize(costFunction, chromSize, popSize, selectionRate, mutRate, **kwargs):
    #     kwargs.setdefault('pairing', 'rank_weighting')
    #     kwargs.setdefault('pairingTounamentSize', 3)
    #     kwargs.setdefault('crossover', 'single_point')
    #     kwargs.setdefault('uniformCrossoverProb', 0.5)

    #     popKeepSize = round(selectionRate*popSize)
    #     pop = np.round(np.random.rand(popSize, chromSize))
    #     numPairs = np.ceil((popSize-popKeepSize)/2)
    #     generation = 0
        
    #     while True:
    #         print("Generation: {}".format(generation))

    #         costs = np.array([costFunction(chrom) for chrom in pop])
    #         sortIndexes = np.argsort(costs)
    #         costs = costs[sortIndexes]
    #         pop = pop[sortIndexes]

    #         for (chrom, cost) in zip(pop, costs):
    #             print("  {0} ..... {1}".format(re.sub(r'\D', '', str(chrom)), cost))

    #         popKeep = pop[:popKeepSize]
    #         parents1, parents2 = selectPairs(popKeep, costs, numPairs,
    #                                          kind=kwargs['pairing'],
    #                                          tournamentSize=kwargs['pairingTounamentSize'])
    #         children = crossover(parents1, parents2, 
    #                              kind=kwargs['crossover'],
    #                              uniformProb=kwargs['uniformCrossoverProb'])[:popSize-popKeepSize]
    #         pop = np.concatenate([popKeep,children], axis=0)

    #         yield pop
            
    #         mutation(pop, np.ceil((popSize-1)*chromSize*mutRate))
    #         generation+=1

    # def selectPairs(popKeep, costs, numberPairs, kind='rank_weighting', **kwargs):
    #     kwargs.setdefault('tournamentSize', 3)
        
    #     popKeepSize = len(popKeep)
    #     numberPairs = int(numberPairs)
    #     if kind == 'top_to_bottom':
    #         p1 = np.arange(0, popKeepSize, 2)[:numberPairs]
    #         p2 = p1 + 1
    #     elif kind == 'random':
    #         p1 = np.random.choice(popKeepSize, numberPairs)
    #         p2 = np.random.choice(popKeepSize, numberPairs)
    #     elif kind == 'cost_weighting':
    #         costs = (costs-costs[popKeepSize])[:popKeepSize]
    #         costsSum = np.sum(costs[:popKeepSize])
    #         if costsSum == 0:
    #             return selectPairs(popKeep, costs, numberPairs, kind='random')
    #         prob = costs/costsSum
    #         cumProb = np.cumsum(prob)
    #         random1 = np.random.rand(numberPairs)
    #         random2 = np.random.rand(numberPairs)
    #         p1 = [argfirst(lambda n : n > r, cumProb) for r in random1]
    #         p2 = [argfirst(lambda n : n > r, cumProb) for r in random2]
    #         for i in range(len(p1)):
    #             if p1[i] == p2[i] :
    #                 p2[i] = np.random.choice(popKeepSize)
    #     elif kind == 'rank_weighting':
    #         ranks = list(range(popKeepSize))
    #         ranksSum = np.sum(ranks)
    #         prob = [(popKeepSize-i-1)/ranksSum for i in ranks]
    #         cumProb = np.cumsum(prob)
    #         random1 = np.random.rand(numberPairs)
    #         random2 = np.random.rand(numberPairs)
    #         p1 = [argfirst(lambda n : n > r, cumProb) for r in random1]
    #         p2 = [argfirst(lambda n : n > r, cumProb) for r in random2]
    #         for i in range(len(p1)):
    #             if p1[i] == p2[i] :
    #                 p2[i] = np.random.choice(popKeepSize)
    #     elif kind == 'tournament':
    #         p1 = []
    #         p2 = []
    #         for _ in range(numberPairs):
    #             group1 = np.random.choice(popKeepSize, kwargs['tournamentSize'])
    #             group2 = np.random.choice(popKeepSize, kwargs['tournamentSize'])
    #             p1.append(np.argmin(costs[group1]))
    #             p2.append(np.argmin(costs[group2]))

    #     return (popKeep[p1], popKeep[p2])

    # def crossover(parents1, parents2, kind='single_point', **kwargs):
    #     kwargs.setdefault('uniformProb', 0.5)
    #     children = []
    #     if kind == 'single_point':
    #         for p1, p2 in zip(parents1,parents2):
    #             crossoverPoint = np.random.choice(len(p1)-1)+1
    #             # pylint: disable=unbalanced-tuple-unpacking
    #             p1Left, p1Right = np.split(p1, [crossoverPoint])
    #             p2Left, p2Right = np.split(p2, [crossoverPoint])
    #             c1 = np.concatenate([p1Left, p2Right])
    #             c2 = np.concatenate([p2Left, p1Right])
    #             children += [c1, c2]
    #     elif kind == 'double_point':
    #         for p1, p2 in zip(parents1,parents2):
    #             crossoverPoints = np.sort(np.random.choice(len(p1)-1, 2, replace=False)+1)
    #             # pylint: disable=unbalanced-tuple-unpacking
    #             l1, m1, r1 = np.split(p1, crossoverPoints)
    #             l2, m2, r2 = np.split(p2, crossoverPoints)
    #             c1 = np.concatenate([l1, m2, r1])
    #             c2 = np.concatenate([l2, m1, r2])
    #             children += [c1, c2]
    #     elif kind == 'uniform':
    #         for p1, p2 in zip(parents1, parents2):
    #             prob = kwargs['uniformProb']
    #             aux = list(map(lambda x: int(x >= prob), np.random.rand(len(p1))))
    #             pair = [p1, p2]
    #             c1 = np.array([pair[aux[i]][i] for i in range(len(p1))])
    #             c2 = np.array([pair[::-1][aux[i]][i] for i in range(len(p1))])
    #             children += [c1, c2]
    #     return children

    # def mutation(pop, numMut):
    #     popSize = len(pop)
    #     chromSize = len(pop[0])
    #     chrom = np.random.choice(popSize-1, int(numMut))+1
    #     bit = np.random.choice(chromSize, int(numMut))
    #     for i, j in zip(chrom, bit):
    #         pop[i,j] = np.abs(pop[i,j]-1)

    # def argfirst(condition, iterable):
    #     return next(x[0] for x in enumerate(iterable) if condition(x[1]))