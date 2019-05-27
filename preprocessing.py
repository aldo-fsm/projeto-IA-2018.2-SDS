import pandas as pd

from fitness import FuncaoRelevancia, FuncaoViabilidade
from constants import RELEVANCY_WEIGHTS, VIABILITY_WEIGHTS

def preprocessGA(dataset, relevancy_constant, viability_constant):
    result = pd.DataFrame()
    R = FuncaoRelevancia(RELEVANCY_WEIGHTS)
    V = FuncaoViabilidade(VIABILITY_WEIGHTS)

    relevancy = dataset.apply(R, axis=1)
    viability = dataset.apply(V, axis=1)
    result['individual_fitness'] = relevancy_constant*relevancy + viability_constant*viability
    
    return result