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
                
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label('Intake type', style={'font-weight': 'bold'}),
                            dcc.Dropdown(id = 'map-dp1', value = 'All', options = ['All', 'Stray', 'Owner Surrender', 'Public Assist', 'Euthanasia Request'], placeholder = 'Intake type',  style = {'order': '1', 'width': '12vw', 'margin-right': '4vw'})]),
                        html.Div([   
                            html.Label('Intake condition', style={'font-weight': 'bold'}),
                            dcc.Dropdown(id = 'map-dp2', value = 'All', options = ['All', 'Nursing', 'Normal', 'Sick', 'Injured', 'Feral', 'Pregnant', 'Other', 'Aged'], placeholder = 'Intake condition',  style = {'order': '2', 'width': '12vw'})])], style = {'order': '1', 'display': 'flex', 'flex-direction': 'row', 'margin-bottom': '1vh', 'justify-content': 'space-around'}),
                    html.Div(id = 'mapbox', children = [], style = {'order': '2', 'width': '50vw'})], style = {'order': '2', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'margin-left': '5vw'})],
            style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center','width':'50%'})

@callback(Output('mapbox', 'children'),
          Input('store-data', 'data'),
          Input('map-dp1', 'value'),
          Input('map-dp2', 'value'))
def update_mapbox(data, value1, value2):
    df = pd.DataFrame(data)
    if (value1 == 'All') & (value2 == 'All'):
        df = df
    elif (value1 != 'All') & (value2 == 'All'):
        df = df[df['intake_type'] == value1]
    elif (value1 == 'All') & (value2 != 'All'):
        df = df[df['intake_condition'] == value2]
    else:
        df = df[(df['intake_condition'] == value2) & (df['intake_type'] == value1)]
    return dcc.Graph(id = 'map-plot', figure = plots.get_map_box(df), style = {'order': '2'})
