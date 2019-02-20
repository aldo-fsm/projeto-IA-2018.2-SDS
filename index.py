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
from apps import ranking, table_select

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
],  className="container")

app.layout = html.Div([
    dcc.Store(id='storage', storage_type='memory', data={}),
    dbc.Tabs(
        [
            dbc.Tab(table_select.layout, label="Dataset"),
            dbc.Tab(ranking.layout, label="Ranking"),
            dbc.Tab(tab1_content, label="Tab 2"),
        ]
    )
])

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
    app.run_server(debug=True, port=8051)