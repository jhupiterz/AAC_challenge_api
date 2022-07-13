from turtle import width
import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from AAC_challenge import plots, utils

import pandas as pd

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='Explore data', style = {'color': 'black'}),

    dcc.Store(id='store-data', data = utils.read_json_data('../raw_data/merged_with_locations.json'), storage_type = 'memory'),

    dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Cats", tab_id="cats"),
                    dbc.Tab(label="Dogs", tab_id="dogs"),
                ],
                id="card-tabs",
                active_tab="cats",
            )
        ),
        dbc.CardBody(html.P(id="card-content", className="card-text")),
    ]
)])

@callback(Output('card-content', 'children'),
          Input('card-tabs', 'active_tab'),
          Input('store-data', 'data'))

def render_tab_content(tab_value, data):
    if tab_value == 'cats':
        df = pd.DataFrame(data)
        return html.Div(children = [
                html.Div([
                        dcc.Graph(figure = plots.get_outcome_timeseries(df), className = 'timeseries-plot'),
                        dcc.Graph(figure = plots.get_has_name_histogram(df), className = 'hasname-plot')], style = {'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),

            plots.get_mapbox(df)], style = {'display': 'flex', 'flex-direction': 'row', 'align-times': 'center','width':'50%' })
