import pandas as pd

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from sklearn import utils

app = dash.Dash(
    __name__, suppress_callback_exceptions = True,
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
                        html.A(
                            "Explore", 
                            href="https://jhupiterz.notion.site/The-Biosignature-Database-f48effd1004f4155acfd76deee382436",
                            target='_blank', 
                            className="doc-link"
                        ),
                        html.A(
                            "Predict",
                            href="https://github.com/jhupiterz/biosignatureDB",
                            target='_blank',
                            className="doc-link"
                        ),
                        html.A(
                            "Documentation",
                            href="https://github.com/Joannaakl27/AAC_challenge",
                            target='_blank',
                            className="doc-link"
                        )
                    
                    ],
                    className="navbar"
                ),
            ],
            className="banner",
        ),
        
        dcc.Store(id='store-data', data = utils.read_json_data('../raw_data/merged_with_locations.json'), storage_type = 'memory'),

        # Main content ----------------------------------------------------------
        html.Div([])
    ]
)

merged_with_locations = utils.read_json_data('../raw_data/merged_with_locations.json')
data = pd.DataFrame(merged_with_locations)

# Runs the app ------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)