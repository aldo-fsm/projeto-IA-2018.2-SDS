import numpy as np
from utils.attribute_utils import evadido, diasAposEvasao, periculosidade,\
    prioritario, qtdProcessos, totalVitmasConsumado, totalVitmasTentado,\
    prisaoPreventiva, prisaoCondenatoria, mpCVLI, enderecoConhecido,\
    prisaoDecretada, diasAposExpedicaoMandado, mandadoAtivo, carcerario,\
    possuiRG, possuiFoto

class FuncaoRelevancia:
    def __init__(self, pesos):
        self.pesos = pesos
        
    def __call__(self, row):
        EV = evadido(row)
        Tev = diasAposEvasao(row) 
        P = periculosidade(row)
        AP = prioritario(row)
        QP = qtdProcessos(row)
        TVC = totalVitmasConsumado(row)
        TVT = totalVitmasTentado(row)
        PP = prisaoPreventiva(row)
        PC = prisaoCondenatoria(row)
        CVLImp = mpCVLI(row)
        #Pcvli = probabilidadeCVLI(row)
        Xr = np.array([EV, 1-np.tanh(Tev), P, AP, QP, TVC, TVT, PP, PC, CVLImp])
        return np.average(Xr, weights=self.pesos)

class FuncaoViabilidade:
    def __init__(self, pesos):
        self.pesos = pesos

    def __call__(self, row):
        EC = enderecoConhecido(row)
        FT = possuiFoto(row)
        RG = possuiRG(row)
        PD = prisaoDecretada(row)
        Texp = diasAposExpedicaoMandado(row)
        MA = mandadoAtivo(row)
        SC = carcerario(row)
        Xv = np.array([EC, FT, RG, PD, 1-np.tanh(Texp), MA, SC])
        return np.average(Xv, weights=self.pesos)

class FitnessMult:
    def __init__(self, Cg, Cv, Cind, Kr, Kv, dataset):
        self.Cg = Cg
        self.Cind = Cind
        self.Cv = Cv
        self.G = lambda x : 0 # falta implementar
        self.R = FuncaoRelevancia(Kr)
        self.V = FuncaoViabilidade(Kv)
        self.dataset = dataset

    def _fitness_ind(self, row):
        relevancy = self.R(row)
        viability = self.V(row)
        return (1-np.exp(-viability/self.Cv))*relevancy

    def __call__(self, chromossome):
        data = self.dataset.iloc[chromossome]
        if len(data) == 0:
            return -np.inf
        group = self.G(data)
        individual = np.mean(data.apply(self._fitness_ind, axis=1).values)
        return self.Cg*group + self.Cind*individual

class FitnessSum:
    def __init__(self, Cg, Cr, Cv, Kr, Kv, dataset):
        self.Cg = Cg
        self.Cr = Cr
        self.Cv = Cv
        self.G = lambda x : 0 # falta implementar
        self.R = FuncaoRelevancia(Kr)
        self.V = FuncaoViabilidade(Kv)
        self.dataset = dataset

    def __call__(self, chromossome):
        data = self.dataset.iloc[chromossome]
        if len(data) == 0:
            return -np.inf
        grouping = self.G(data)
        relevancy = np.mean(data.apply(self.R, axis=1).values)
        viability = np.mean(data.apply(self.V, axis=1).values)
        return self.Cg*grouping + self.Cr*relevancy + self.Cv*viability