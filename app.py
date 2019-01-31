import dash
import dash_bootstrap_components as dbc
from flask import Flask, send_from_directory

server = Flask(__name__)
app = dash.Dash(__name__, server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions']=True
