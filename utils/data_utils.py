import pandas as pd
from constants import DATASET_PATH

def load_dataset(only_actives=True):
    dataset = pd.read_excel(DATASET_PATH)
    if only_actives:
        dataset = dataset.loc[dataset['SITUAÇÃO DO MANDADO'] == 'ATIVO']
    return dataset