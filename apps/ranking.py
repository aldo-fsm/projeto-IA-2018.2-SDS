import dash
import dash_core_components as dcc
import dash_html_components as html

from app import app

border = {'border-width': '1px', 'border-style' : 'solid'}

layout = html.Div([
    html.Div([
        html.Div([
                html.Div([
                    'A'
                ], className='row', style=border),
                html.Div([
                    'B'
                ], className='row', style=border)
        ], className='col-5 mr-auto', style=border),
        html.Div([
            'B'
        ], className='col-5', style=border)
    ], className='row'),
], className='container')