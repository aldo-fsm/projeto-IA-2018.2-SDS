import pandas as pd
import numpy as np
from constants import DATASET_PATH

DEFAULT_DATASET = 'BD_SITE_SCC_projeto_UPE_unificada.xlsx'

def load_dataset(path, only_actives=True):
    dataset = pd.read_excel(path)
    dataset = dataset.loc[dataset['STATUS CARCERÁRIO'] != 'DUPLICIDADE']
    if only_actives:
        dataset = dataset.loc[dataset['SITUAÇÃO DO MANDADO'] == 'ATIVO']
    return dataset

'''
def add_identifier(dataset):
    def gen_id(row):
        if pd.notnull(row['NOME']) and pd.notnull(row['NOME DA MÃE']) and pd.notnull(row['DATA DE NASCIMENTO']):
            return str(row['NOME'])+str(row['NOME DA MÃE'])+str(row['DATA DE NASCIMENTO'])
        else:
            return np.nan
    identifiers = dataset.apply(gen_id, axis=1)
    return pd.concat([identifiers.rename('ID'), dataset], axis=1)
'''