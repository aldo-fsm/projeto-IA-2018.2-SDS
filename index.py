import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd

from app import app
from apps import ranking

app.layout = html.Div([
    dcc.Tabs(id="navbar", children=[
        dcc.Tab(label='Tab One', value="ranking"),
        dcc.Tab(label='Tab Two', value="1"),
    ]),
    html.Div(id='tabs-content')
])

tab1_content = html.Div([
    dbc.Card(
        dbc.CardBody(
            [
                dbc.CardText("This is tab 1!"),
                dbc.Button("Click here", color="success"),
            ]
        ),
        className="mt-3",
    ),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arraste ou ',
            html.A('Selecione uma Tabela')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
],  className="container")


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

app.layout = html.Div([
    dbc.Tabs(
        [
            dbc.Tab(tab1_content, label="Tab 1"),
            dbc.Tab(ranking.layout, label="Tab 2"),
        ]
    )
])

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Link", href="#")),
#         dbc.DropdownMenu(
#             nav=True,
#             in_navbar=True,
#             label="Menu",
#             children=[
#                 dbc.DropdownMenuItem("Entry 1"),
#                 dbc.DropdownMenuItem("Entry 2"),
#                 dbc.DropdownMenuItem(divider=True),
#                 dbc.DropdownMenuItem("Entry 3"),
#             ],
#         ),
#     ],
#     brand="Demo",
#     brand_href="#",
#     sticky="top",
# )

# body = dbc.Container(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(
#                     [
#                         html.H2("Heading"),
#                         html.P(
#                             """\
# Donec id elit non mi porta gravida at eget metus.
# Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum
# nibh, ut fermentum massa justo sit amet risus. Etiam porta sem
# malesuada magna mollis euismod. Donec sed odio dui. Donec id elit non
# mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus
# commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit
# amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed
# odio dui."""
#                         ),
#                         dbc.Button("View details", color="secondary"),
#                     ],
#                     md=4,
#                 ),
#                 dbc.Col(
#                     [
#                         html.H2("Graph"),
#                         dcc.Graph(
#                             figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}
#                         ),
#                     ]
#                 ),
#             ]
#         )
#     ],
#     className="mt-4",
# )
# app.layout = html.Div([navbar, body])


if __name__ == '__main__':
    app.run_server(debug=True)