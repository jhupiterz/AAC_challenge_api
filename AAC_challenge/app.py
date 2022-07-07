import pandas as pd

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from AAC_challenge import utils

app = dash.Dash(
    __name__, suppress_callback_exceptions = True,
    use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1", 'charSet':'“UTF-8”'}])

app.title = "AAC Dashboard"

app.layout = html.Div(
    [
        # Banner ------------------------------------------------------------
        html.Div(
            [
                html.A(
                    [
                        html.Img(
                            src="/assets/aac.jpeg",
                            alt="AAC"
                        ),
                        html.H3("AAC Dashboard")
                    ],
                    href="https://www.austintexas.gov/austin-animal-center",
                    target='_blank',
                    className="logo-banner",
                ),
                html.Div(
                    [
                        dbc.DropdownMenu(
                            [
                                dbc.DropdownMenuItem("Explore", href = "/explore"),
                                dbc.DropdownMenuItem("Predict", href = '/predict'),
                                dbc.DropdownMenuItem("Documentation", href = '/docs')
                            ],
                            label="MENU",
                            size = 'lg',
                            className="mb-3"
                        )
                    
                    ],
                    className="navbar"
                ),
            ],
            className="banner",
        ),

        # Main content ----------------------------------------------------------
        html.Div([]),

        dash.page_container
    ]
)

merged_with_locations = utils.read_json_data('../raw_data/merged_with_locations.json')
data = pd.DataFrame(merged_with_locations)

# Runs the app ------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)