import numpy as np
from utils.attribute_utils import evadido, diasAposEvasao, periculosidade,\
    prioritario, qtdProcessos, totalVitmasConsumado, totalVitmasTentado,\
    prisaoPreventiva, prisaoCondenatoria, mpCVLI, enderecoConhecido,\
    qtdPrisaoDecretadas, diasAposExpedicaoMandado, carcerario,\
    possuiRG, possuiFoto

class FuncaoRelevancia:
    def __init__(self, pesos):
        self.pesos = pesos
        
    def __call__(self, row):
        return np.average(row, weights=self.pesos)

class FuncaoViabilidade:
    def __init__(self, pesos):
        self.pesos = pesos

    def __call__(self, row):
        return np.average(row, weights=self.pesos)

# class FitnessMult:
#     def __init__(self, Cg, Cv, Cind, Kr, Kv, dataset):
#         self.Cg = Cg
#         self.Cind = Cind
#         self.Cv = Cv
#         self.G = lambda x : 0 # falta implementar
#         self.R = FuncaoRelevancia(Kr)
#         self.V = FuncaoViabilidade(Kv)
#         self.dataset = dataset

#     def _fitness_ind(self, row):
#         relevancy = self.R(row)
#         viability = self.V(row)
#         return (1-np.exp(-viability/self.Cv))*relevancy

#     def __call__(self, chromossome):
#         data = self.dataset.iloc[chromossome]
#         if len(data) == 0:
#             return -np.inf
#         group = self.G(data)
#         individual = np.mean(data.apply(self._fitness_ind, axis=1).values)
#         return self.Cg*group + self.Cind*individual

class FitnessSum:
    def __init__(self, grouping_constant, dataset):
        self.grouping_constant = grouping_constant
        self.dataset = dataset

    def __call__(self, chromossome):
        data = self.dataset.iloc[chromossome]
        if len(data) == 0:
            return -np.inf
        if 'cluster' in data:
            grouping = groupingFactor(data)
        else:
            grouping = 0
        return data.individual_fitness.mean() + self.grouping_constant*grouping
        
def groupingFactor(data):
    num_clusters = len(data.cluster.unique())
    return 1 - num_clusters/data.shape[0]
