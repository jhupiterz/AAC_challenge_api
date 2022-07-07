import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output

from AAC_challenge import plots, utils

import pandas as pd

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='Explore data', style = {'color': 'black'}),

    dcc.Store(id='store-data', data = utils.read_json_data('../raw_data/merged_with_locations.json'), storage_type = 'memory'),

    html.Div([
            dcc.Tabs(id="tabs", value = 'cats', className= "tabs",
                        children=[
                dcc.Tab(label=' Cats ', value='cats',
                        className= "single-tab", selected_className= "single-tab-selected"),
                dcc.Tab(label=' Dogs ', value='dogs',
                        className= "single-tab", selected_className= "single-tab-selected")
                ])
            ], className= "tabs-container"),
        
            html.Br(),
            html.Div(id='tab-content')
])

@callback(Output('tab-content', 'children'),
          Input('tabs', 'value'),
          Input('store-data', 'data'))
def render_tab_content(tab_value, data):
    if tab_value == 'cats':
        df = pd.DataFrame(data)
        return html.Div(children = [
            dcc.Graph(figure = plots.get_outcome_timeseries(df), className = 'timeseries-plot'),
            plots.get_mapbox(df)], style = {'display': 'flex', 'flex-direction': 'row', 'align-times': 'center'})