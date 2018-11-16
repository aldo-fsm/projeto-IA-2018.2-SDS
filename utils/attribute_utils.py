import time
import dateutil
from datetime import datetime
import pandas as pd

PARSER_INFO = dateutil.parser.parserinfo(dayfirst=True, yearfirst=False)

def getTodayDate():
    return dateutil.parser.parse(time.ctime())

def daysEvaded(row):
    field = row['DATA DE EVASÃO DO SISTEMA CARCERÁRIO']
    if isEvaded(row) and not pd.isnull(field):
        today = getTodayDate()
        if isinstance(field, datetime):
            evasion_date = field
        elif isinstance(field, str):
            evasion_date = dateutil.parser.parse(field, PARSER_INFO)
        else:
            raise ValueError('A data de evasão deve ser do tipo string ou datetime.')
        return (today-evasion_date).days
    else:
        return 0

def isEvaded(row):
    return int(row.AIS.lower() == 'evadidos')

def dangerousness(row):
    return row['PERICULOSIDADE (BI - MP - PROCESSO)']

def isPrioritary(row):
    field = row['ALVO PRIORITÁRIO']
    return int(not pd.isnull(field))