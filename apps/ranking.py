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

from utils.data_utils import load_dataset

import constants

UPLOAD_DIRECTORY = "./datasets"

df = None
ranking_progress = 1

def rank(dataset, V, R, G, som_attrs, rank_length, pop_size=30, generations_to_run=100):
    global ranking_progress
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
        optimizer.step(fitness_function)
        ranking_progress = i/generations_to_run
    ranking_progress = 1
    return optimizer

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


layout = html.Div([
    dcc.Interval(
            id='ranking-progress-update',
            interval=1000
    ),
    html.H1("Ranqueamento"),
    html.Div([
        html.Div([
            html.Div([
                dcc.Location(id='url', refresh=False),
                html.H2("Upload de Tabelas"),
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(
                        ["Arraste ou selecione tabelas para upload."]
                    ),
                    style={
                        "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                    },
                    multiple=True,
                ),
            ]),
            html.Div([
                html.H2("Lista de Tabelas"),
                html.Div([
                    dbc.RadioItems(id="file-radioitems")
                ], id='file-list'),
                html.Button('Limpar', id='clear-btn'),
                ], className='mt-3'),
                html.Div([
                    html.H2("Parâmetros"),
                        # dbc.Col([
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
                                dcc.Slider(value=0.5, step=0.01, min=0, max=1, marks={0:'0', 1:'1'}, id='G-slider'),
                                dbc.Checklist(
                                    options=[
                                        {'label': attr, 'value': attr} for attr in ['IAS']
                                    ],
                                    values=[],
                                    className='mt-3'
                                )
                            ])
                        ], className='mt-3'),
            ], className='mt-3'),
        ], className='mr-3', style={"max-width": "500px"}),
        html.Div([
            html.H2("Tabela Selecionada"),
            dbc.Card([
                dbc.CardHeader(id='file-card-header'),
                dbc.CardBody([
                    html.P('', id='file-content', style={'white-space' : 'pre-line'})
                ], style={'overflowY': 'scroll', 'height': '60vh'})
            ])
        ], className="col-8")
    ], className="row mt-5"),
    html.Div([
        dbc.Button(id='rank-button'),
    ], id='button-progress', className='d-flex justify-content-center'),
    html.Div([
        html.Div([
            html.Div([
                dbc.Progress(value=ranking_progress, id='ranking-progress'),
            ],id='result')
        ], className="col-8")
    ], className="row mt-5"),
], className="container mt-3")


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def remove_uploaded_files():
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            os.remove(path)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=filename)

@app.callback(Output('ranking-progress', 'value'),
             [Input('ranking-progress-update', 'n_intervals')])
def update_progress(n_intervals):
    global ranking_progress
    return str(ranking_progress*100)

@app.callback(Output('button-progress', 'children'),
             [Input('ranking-progress', 'value')])
def button_progress(progress):
    if progress == '100':
        return  dbc.Button('Ranquear', id='rank-button', color="success")
    else:
        return dbc.Progress(value=ranking_progress, id='ranking-progress')
import time
@app.callback(Output('result', 'children'),
            [Input('rank-button', 'n_clicks')],
            [State('V-slider', 'value'),
             State('R-slider', 'value'),
             State('G-slider', 'value')])
def on_rank_btn_click(n_clicks, V, R, G):
    print(n_clicks, V, R, G)
    global ranking_progress
    if n_clicks:
        ranking_progress = 0
        for i in range(100):
            print(i)
            time.sleep(0.5)
            ranking_progress += .01
        ranking_progress = 1
        return "alsdjadkljsdlajkdsldkajldajd"
    return ''

last_n_clicks = None

@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents"), Input("clear-btn", "n_clicks")],
)
def update_output(uploaded_filenames, uploaded_file_contents, n_clicks):
    """Save uploaded files and regenerate the file list."""
    global last_n_clicks
    if n_clicks != last_n_clicks:
        remove_uploaded_files()
        last_n_clicks = n_clicks
    elif uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            name = 'BD_SITE_SCC_projeto_UPE_unificada.xlsx'
            save_file(name, data)
    files = uploaded_files()
    if len(files) == 0:
        return "No files yet!"
    else:
        return [dbc.RadioItems(id="file-radioitems", options=[{'label': filename, 'value': filename} for filename in files])]


@app.callback(Output('file-content', 'children'),
              [Input('file-radioitems', 'value')])
def display_file(filename):
    if filename:
        try:
            global df
            df = load_dataset(os.path.join(UPLOAD_DIRECTORY, filename))
            return dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.astype(str).to_dict("rows"),
                    style_table={'overflowX': 'scroll'},
                )
        except:
            return ''
    return ''


@app.callback(Output('file-card-header', 'children'),
              [Input('file-radioitems', 'value')])
def display_filename(filename):
    if filename:
        return filename
    return 'Nenhuma tabela selecionada'