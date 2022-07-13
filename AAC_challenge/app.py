import pandas as pd

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from AAC_challenge import utils

app = dash.Dash(
    __name__, suppress_callback_exceptions = True,
    use_pages=True, external_stylesheets=[dbc.themes.LITERA],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1", 'charSet':'“UTF-8”'}])

app.title = "AAC Dashboard"

app.layout = html.Div([
    dbc.Navbar(
        dbc.Container([
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/aac.jpeg",
                                         height="35px")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://www.austintexas.gov/austin-animal-center",
                style={"textDecoration": "none"},
            ),
            html.Div([
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("More pages", header=True),
                        dbc.DropdownMenuItem("Home", href="/"),
                        dbc.DropdownMenuItem("Explore", href="/explore"),
                        dbc.DropdownMenuItem("Predict", href='/predict'),
                        dbc.DropdownMenuItem("Documentation", href='/docs')
                    ],
                    nav=True,
                    in_navbar=True,
                    label="More",
                ),
            ], ),
        ])),

    # Main content ----------------------------------------------------------
    html.Div([]),
    dash.page_container
])

merged_with_locations = utils.read_json_data('../raw_data/merged_with_locations.json')
data = pd.DataFrame(merged_with_locations)

# Runs the app ------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
