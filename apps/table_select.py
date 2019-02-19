
import base64
import datetime
import io
import os
import re

from urllib.parse import quote as urlquote
from matplotlib import pyplot as plt

from flask import send_from_directory

import dash
from dash.exceptions import PreventUpdate
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

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


layout = html.Div([
    html.H1("Seleção da base de dados"),
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
                    multiple=False,
                ),
            ]),
            html.Div([
                html.H2("Lista de Tabelas"),
                html.Div([
                    dbc.RadioItems(id="file-radioitems")
                ], id='file-list'),
                html.Button('Limpar', id='clear-btn'),
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
], className="container mt-3")


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=filename)

# @app.callback(Output('ranking-progress', 'value'),
#              [Input('ranking-progress-update', 'n_intervals')])
# def update_progress(n_intervals):
#     global ranking_progress
#     return str(ranking_progress*100)

# @app.callback(Output('button-progress', 'children'),
#              [Input('ranking-progress', 'value')])
# def button_progress(progress):
#     if progress == '100':
#         return  dbc.Button('Ranquear', id='rank-button', color="success")
#     else:
#         return dbc.Progress(value=ranking_progress, id='ranking-progress')

@app.callback(
    Output("session-store", "data"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
    [State("session-store", "data")],
)
def update_output(uploaded_filename, uploaded_file_contents, data):
    data = data or {'dataset': {'table_name': None, 'data': None}}
    if uploaded_filename is not None and uploaded_file_contents is not None:
        print(uploaded_filename)
        data['dataset'] = {'table_name':  uploaded_filename, 'data': uploaded_file_contents}
    return data

@app.callback(Output('file-content', 'children'),
              [Input('session-store', 'data')])
def display_file(data):
    dataset = data.get('dataset')
    print('aaaa')
    if False:#dataset.get('data'):
        try:
            df = parse_contents(data.get('dataset').get('data'), dataset.get('table_name'))
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
             [Input('session-store', 'modified_timestamp')],
             [State('session-store', 'data')])
def display_filename(ts, data):
    print(ts)
    if ts is None:
            raise PreventUpdate
    filename = data.get('dataset').get('table_name')
    print(filename)
    if filename:
        return filename
    return 'Nenhuma tabela selecionada'