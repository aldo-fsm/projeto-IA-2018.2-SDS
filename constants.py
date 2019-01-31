import numpy as np


DATASET_PATH = 'datasets/' # Baixar dados no drive e colocar na pasta datasets

RELEVANCY_WEIGHTS = np.array([
    70,	 # Evadido
    80,	 # Dias após evasão
    100, # Perículosidade
    100, # Alvo prioritário
    40,	 # Qtd processos
    50,	 # Total de vítimas - consumado
    50,	 # Total de vítimas - tentado
    60,	 # Preventiva
    100, # Condenatória
    90,	 # MP CVLI
#    80	 # Probabilidade de cometer CVLI
])

VIABILITY_WEIGHTS = np.array([
    100, # Endereço conhecido
    100, # Foto
    100, # RG no sistema
    60,	 # Número de mandados de prisão decretados
    80,	 # Data da expedição próxima
    100, # Sistema carcerário
#    90,	 # Quantidade de bases de dados
])