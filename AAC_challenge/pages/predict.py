import dash
from dash import html, dcc

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='This is our dashboard page', style = {'color': 'black'}),

    html.P(children='This is our dashboard page content.', style = {'color': 'black'}),

])