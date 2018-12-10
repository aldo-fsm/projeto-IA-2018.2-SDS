import time
import dateutil
from datetime import datetime
import pandas as pd

PARSER_INFO = dateutil.parser.parserinfo(dayfirst=True, yearfirst=False)

def getTodayDate():
    return dateutil.parser.parse(time.ctime())

def elapsedTime(date):
    today = getTodayDate()
    if not isinstance(date, datetime):
        try:
            date = dateutil.parser.parse(date, PARSER_INFO)
        except:
            #raise ValueError('date deve ser do tipo string ou datetime.')
            return getTodayDate()-getTodayDate() # solução temporária para testes (alguns campos de datas estão vindo como números inteiros - Ex.: 4236)
    return today-date

def diasAposEvasao(row):
    field = row['DATA DE EVASÃO DO SISTEMA CARCERÁRIO']
    if evadido(row) and not pd.isnull(field):
        return elapsedTime(field).days
    else:
        return 0

def evadido(row):
    return int(row.AIS.lower() == 'evadidos')

def periculosidade(row):
    return row['PERICULOSIDADE (BI - MP - PROCESSO)']

def prioritario(row):
    field = row['ALVO PRIORITÁRIO']
    return int(not pd.isnull(field))

def qtdProcessos(row):
    field = row['QUANTIDADE DE PROCESSOS NO TJPE']
    return field if not pd.isnull(field) else 0

def totalVitmasConsumado(row):
    field = row['TOTAL DE VÍTIMAS-CONSUMADO']
    return field if not pd.isnull(field) else 0

def totalVitmasTentado(row):
    field = row['TOTAL DE VÍTIMAS-TENTADO']
    return field if not pd.isnull(field) else 0

def prisaoPreventiva(row):
    field = row['TIPO DE PRISÃO DECRETADA']
    return 1 if field == 'PREVENTIVA' else 0

def prisaoCondenatoria(row):
    field = row['TIPO DE PRISÃO DECRETADA']
    return 1 if field == 'CONDENATÓRIA' else 0

def mpCVLI(row):
    field = row['MP CVLI']
    return field if not pd.isnull(field) else 0

#def probabilidadeCVLI(???):
#    ???

def enderecoConhecido(row):
    field = row['ENDEREÇO DO ALVO']
    return int(not pd.isnull(field))

def possuiFoto(row):
    field = row['FOTOS']
    return int(field == 'SIM')

def possuiRG(row):
    field = row['RG NO SISTEMA']
    return int(field == 'SIM')

def prisaoDecretada(row):
    field = row['TIPO DE PRISÃO DECRETADA']
    return int(not pd.isnull(field))

def diasAposExpedicaoMandado(row):
    field = row['DATA EXPEDIÇÃO DO MANDADO']
    if not pd.isnull(field):
        return elapsedTime(field).days
    else:
        return 0

def carcerario(row):
    field = row['CARCERÁRIO']
    return int(not pd.isnull(field))

# DESNECESSÁRIO
#def mandadoAtivo(row):
#    field = row['SITUAÇÃO DO MANDADO']
#    return int(field == 'ATIVO')
#--------------


