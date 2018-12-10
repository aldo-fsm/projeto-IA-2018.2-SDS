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
    return int(row['STATUS CARCERÁRIO'] == 'EVADIDO')

def periculosidade(row):
    return float(row['PERICULOSIDADE (BI - MP - PROCESSO)'])

def prioritario(row):
    field = row['ALVO PRIORITÁRIO']
    return int(not pd.isnull(field))

def qtdProcessos(row):
    field = int(row['QUANTIDADE DE PROCESSOS NO TJPE']) + int(row['SUBTOTAL PROCESSOS'])
    return field if not pd.isnull(field) else 0

def qtdBasesDados(row):
    field = row['TOTAL BASES']
    return int(field) if not pd.isnull(field) else 0

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
    field = row['N. RG']
    return int(not pd.isnull(field))

def qtdPrisaoDecretadas(row):
    field = row['SUBTOTAL MP']
    return int(field)

def diasAposExpedicaoMandado(row):
    field = row['DATA EXPEDIÇÃO DO MANDADO']
    if not pd.isnull(field):
        return elapsedTime(field).days
    else:
        return 0

def carcerario(row):
    field = row['PRONTUÁRIO SERES']
    return int(not pd.isnull(field))

# DESNECESSÁRIO
#def mandadoAtivo(row):
#    field = row['SITUAÇÃO DO MANDADO']
#    return int(field == 'ATIVO')
#--------------


