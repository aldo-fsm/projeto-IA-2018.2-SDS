import numpy as np
import utils
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
