
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
    html.H1("Upload de Tabelas"),
    html.Div([
        html.Div([
            # html.H2("Tabela Selecionada"),
            dbc.Card([
                dbc.CardHeader(id='file-card-header'),
                dbc.CardBody([
                    html.Div([
                        dcc.Location(id='url', refresh=False),
                        # html.H2("Upload de Tabelas"),
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
                    # html.P('', id='file-content', style={'white-space' : 'pre-line'})
                ], style={'overflowY': 'scroll', 'width': '40vw'})
            ])
        ], className="row")
    ], className="mt-5"),
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
    Output("storage", "data"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
    [State("storage", "data")],
)
def update_output(uploaded_filename, uploaded_file_contents, data):
    data = data or {}
    if uploaded_filename is not None and uploaded_file_contents is not None:
        data['filename'] = uploaded_filename
        data['file_contents'] = uploaded_file_contents
    print('uploaded')
    return data

@app.callback(Output('file-content', 'children'),
              [Input('storage', 'data')])
def display_file(data):
    # filename, content = data.get('filename'), data.get('file_contents')
    # if filename:
    #     try:
    #         df = parse_contents(content, filename)
    #         print(':)')
    #         return dash_table.DataTable(
    #                 id='table',
    #                 columns=[{"name": i, "id": i} for i in df.columns],
    #                 data=df.astype(str).to_dict("rows"),
    #                 style_table={'overflowX': 'scroll'},
    #             )
    #     except:
    #         print(':(')
    #         return ''
    return ''


@app.callback(Output('file-card-header', 'children'),
             [Input('storage', 'modified_timestamp')],
             [State('storage', 'data')])
def display_filename(ts, data):
    print(ts)
    filename = data.get('filename')
    print(filename)
    if filename:
        return filename
    return 'Nenhuma tabela selecionada'