import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from apps import ranking

app.layout = html.Div([
    dcc.Tabs(id="navbar", children=[
        dcc.Tab(label='Tab One', value="ranking"),
        dcc.Tab(label='Tab Two', value="1"),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('navbar', 'value')])
def render_content(tab):
    if tab == 'ranking':
        return ranking.layout
    elif tab == '1':
        return html.H1('Dash Tabs component demo')

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == '__main__':
    app.run_server(debug=True)