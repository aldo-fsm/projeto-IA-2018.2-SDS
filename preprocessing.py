import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

from fitness import FuncaoRelevancia, FuncaoViabilidade
from constants import RELEVANCY_WEIGHTS, VIABILITY_WEIGHTS
from clustering.som import run_som
from utils import attribute_utils as attr

def extractRelevancyFeatures(dataset):
    Xr = dataset.apply(lambda row: pd.Series([
        attr.evadido(row),
        attr.diasAposEvasao(row),
        attr.periculosidade(row),
        attr.prioritario(row),
        attr.qtdProcessos(row),
        attr.totalVitmasConsumado(row),
        attr.totalVitmasTentado(row),
        attr.prisaoPreventiva(row),
        attr.prisaoCondenatoria(row),
        attr.mpCVLI(row)
    ]), axis=1)
    Xr = MinMaxScaler().fit_transform(Xr)
    Xr[:, 1] = 1 - Xr[:, 1]
    return Xr

def extractViabilityFeatures(dataset):
    Xv = dataset.apply(lambda row: pd.Series([
        attr.enderecoConhecido(row),
        attr.possuiFoto(row),
        attr.possuiRG(row),
        attr.qtdPrisaoDecretadas(row),
        attr.diasAposExpedicaoMandado(row),
        attr.carcerario(row)
    ]), axis=1)
    Xv = MinMaxScaler().fit_transform(Xv)
    Xv[:, 4] = 1 - Xv[:, 4]
    return Xv

def preprocessGA(dataset, relevancy_constant, viability_constant, grouping_features):
    result = pd.DataFrame()
    R = FuncaoRelevancia(RELEVANCY_WEIGHTS)
    V = FuncaoViabilidade(VIABILITY_WEIGHTS)
    
    relevancy = np.apply_along_axis(R, axis=1, arr=extractRelevancyFeatures(dataset))
    viability = np.apply_along_axis(V, axis=1, arr=extractViabilityFeatures(dataset))
    result['individual_fitness'] = relevancy_constant*relevancy + viability_constant*viability
    
    if len(grouping_features) > 0:
        som_results = run_som(preprocessSOM(dataset, grouping_features), 100, 100)
        result['cluster'] = som_results.cluster

    return result

def preprocessSOM(dataset, selected_features):

    featureNameMapping = {
        'AIS': 'AIS',
        'DATA DA PRISÃO ou REGISTRO NO CARCERÁRIO': 'data de prisão',
        'PRONTUÁRIO SERES': 'prontuário seres',
        'STATUS CARCERÁRIO': 'status evasão',
        'UNIDADE PRISIONAL ATUAL': 'unidade prisional',
        'IDADE': 'idade',
        'BI CVLI': 'BI CVLI',
        'BI CVP': 'BI CVP',
        'QUANTIDADE DE PROCESSOS NO TJPE': 'qtd TJPD',
        'TOTAL DE VÍTIMAS-CONSUMADO': 'total de vítimas',
        'BI TENTATIVA-CVLI': 'BI tentativa cvli',
        'BI OUTROS': 'bi outros',
        'BI NARCOTRÁFICO': 'bi narcotráfico'
    }

    numeric_features = [
        feature for feature in [
            'IDADE',
            'BI CVLI',
            'BI CVP',
            'QUANTIDADE DE PROCESSOS NO TJPE',
            'TOTAL DE VÍTIMAS-CONSUMADO',
            'BI TENTATIVA-CVLI',
            'BI OUTROS',
            'BI NARCOTRÁFICO'
        ] if featureNameMapping[feature] in selected_features]

    categorical_features = [
        feature for feature in [
            'AIS',
            'DATA DA PRISÃO ou REGISTRO NO CARCERÁRIO',
            'PRONTUÁRIO SERES',
            'STATUS CARCERÁRIO',
            'UNIDADE PRISIONAL ATUAL'
        ] if featureNameMapping[feature] in selected_features]

    print('{} numeric and {} categorical features selected'.format(len(numeric_features), len(categorical_features)))

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', MinMaxScaler())])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='nan')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    def handleFloat(number):
        try:
            return float(number)
        except:
            return np.NaN

    df = pd.DataFrame()
    df[numeric_features] = dataset[numeric_features].applymap(handleFloat)
    df[categorical_features] = dataset[categorical_features].astype(str)
    return preprocessor.fit_transform(df).toarray()