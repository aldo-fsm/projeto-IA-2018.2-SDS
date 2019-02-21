import base64
import datetime
import io
import os
import re

from urllib.parse import quote as urlquote
from matplotlib import pyplot as plt

from flask import send_from_directory

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import numpy as np

from app import app, server


from ga.genetic_algorithm import GeneticAlgorithm
from ga.crossover import Crossover
from ga.mutation import Mutation
from ga.selection import Selection
from fitness import FitnessSum

from utils.data_utils import load_dataset, parse_contents

import constants

UPLOAD_DIRECTORY = "./datasets"
ALL_SOM_ATTRS = ['AIS', 'idade', 'BI CVLI', 'BI CVP', 'qtd TJPD', 'status evasão', 'prontuário seres', 'total de vítimas', 'status carcerário', 'BI tentativa cvli', 'bi outros', 'bi narcotráfico', 'data de prisão' , 'unidade prisional']

def rank(dataset, V, R, G, som_attrs, rank_length, pop_size=30, generations_to_run=3):
    print('rank size', rank_length)
    print(dataset.shape)
    ranking_progress = 0
    table_len = dataset.shape[0]
    gene_set = list(range(table_len))
    chr_size = rank_length

    selection = Selection(0.5)
    crossover = Crossover(kind=1)
    mutation = Mutation(0.5)
    optimizer = GeneticAlgorithm(gene_set, selection, crossover, mutation)
    optimizer.initializePopulation(chr_size, pop_size)

    fitness_function = FitnessSum(G, R, V, constants.RELEVANCY_WEIGHTS, constants.VIABILITY_WEIGHTS, dataset)

    for i in range(generations_to_run):
        print(i)
        optimizer.step(fitness_function)
        ranking_progress = i/generations_to_run
        print(ranking_progress)
    ranking_progress = 1
    print(ranking_progress)
    population = optimizer.population
    fitnesses = [fitness_function(chr) for chr in population]
    print(fitnesses)
    best_index = np.argmax(fitnesses)
    best_chr = population[best_index]
    print(best_chr)
    ranking = dataset.iloc[best_chr]
    ind_fitness = ranking.apply(fitness_function.individual_fitness, axis=1).values
    ranking.insert(len(ranking.columns), 'fitness', ind_fitness)
    print('sorting...')
    return ranking.sort_values('fitness', ascending=False)

layout = html.Div([
    html.H1("Ranqueamento"),
    html.Div([
        html.Div([
            html.Div([
                html.H2("Parâmetros"),
                    # dbc.Col([
                dcc.Dropdown(
                    options=[
                        {'label': 'Top {}'.format(i), 'value': i} for i in [5, 10, 20, 50, 100, 500]
                    ],
                    placeholder='Tamanho do ranking',
                    id='rank-size-dropdown'
                ),
                dbc.Card([
                    dbc.CardHeader('Viabilidade'),
                    dbc.CardBody([
                        dcc.Slider(value=0.5, step=0.01, min=0, max=1, marks={0:'0', 1:'1'}, id='V-slider'),
                    ])
                ], className='mt-3'),
                dbc.Card([
                    dbc.CardHeader('Relevância'),
                    dbc.CardBody([
                        dcc.Slider(value=0.5, step=0.01, min=0, max=1, marks={0:'0', 1:'1'}, id='R-slider'),
                    ])
                ], className='mt-3'),
                dbc.Card([
                    dbc.CardHeader('Proximidade'),
                    dbc.CardBody([
                        html.Button(id='toggle-all'),
                        html.Div([
                            dbc.Checklist(
                                options=[
                                    {'label': attr, 'value': attr} for attr in ALL_SOM_ATTRS
                                ],
                                id='som-attrs-checkboxes',
                                values=[],
                            )

                        ], className='mb-3', style={'overflowY': 'scroll', 'height': '20vh'}),
                        dcc.Slider(value=0.5, step=0.01, min=0, max=1, marks={0:'0', 1:'1'}, id='G-slider'),
                    ])
                ], className='mt-3'),
            ], className='mt-3'),
        ], className='col-md-5 mr-3'),
        html.Div([
            html.Div([
                html.H2("Ranking"),
                html.Div([
                    # dbc.Progress(value=ranking_progress, id='ranking-progress'),
                ],id='result', style={'overflowY': 'scroll', 'height': '60vh'})
            ], className='mt-3'),
        ], className='col-md-5'),
    ], className="row mt-5 mb-3"),
    html.Div([
        dbc.Button('Ranquear', id='rank-button'),
    ], id='button-progress', className='d-flex justify-content-center'),
], className="container mt-3")

@app.callback(Output('toggle-all', 'children'),
             [Input('toggle-all', 'n_clicks')])
def change_toggle_btn_text(n_clicks):
    if n_clicks is not None and n_clicks % 2 != 0:
        return 'Desmarcar tudo'
    else:
        return 'Marcar tudo'

@app.callback(Output('som-attrs-checkboxes', 'values'),
             [Input('toggle-all', 'n_clicks')])
def toggle_all_checkboxes(n_clicks):
    if n_clicks is not None and n_clicks % 2 != 0:
        return ALL_SOM_ATTRS
    else:
        return []
        

# @app.callback(Output('button-progress', 'children'),
#              [Input('ranking-progress', 'value')])
# def button_progress(progress):
#     if progress == '100':
#         return  dbc.Button('Ranquear', id='rank-button', color="success")
#     else:
#         return dbc.Progress(value=ranking_progress, id='ranking-progress')
import time
@app.callback(Output('result', 'children'),
            [Input('rank-button', 'n_clicks')],
            [State('storage', 'data'),
             State('V-slider', 'value'),
             State('R-slider', 'value'),
             State('G-slider', 'value'),
             State('som-attrs-checkboxes', 'values'),
             State('rank-size-dropdown', 'value')])
def on_rank_btn_click(n_clicks, data, V, R, G, som_attrs, ranking_size):
    filename, content = data.get('filename'), data.get('file_contents');
    if not filename:
        return ''
    print('parsing dataset...')
    df = parse_contents(content, filename)
    print(n_clicks, V, R, G, som_attrs, ranking_size)
    if n_clicks:
        ranking = rank(df, V, R, G, som_attrs, int(ranking_size))
        print(ranking)
        return dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=ranking.astype(str).to_dict("rows"),
            style_table={'overflowX': 'scroll', 'width':'100%'},
        )
    else:
        return ''