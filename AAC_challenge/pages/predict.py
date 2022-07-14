import dash
from AAC_challenge import plots
import requests
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='Make predictions', style = {'color': 'black'}),

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
        dbc.CardBody(html.P(id="card-content-predict", className="card-text")),
    ]
)])

@callback(Output('card-content-predict', 'children'),
          Input('card-tabs', 'active_tab'))

def render_tab_content(tab_value):
    if tab_value == 'cats':
        return html.Div(children = [

                        html.Div([

                                    dbc.RadioItems(id = 'sex', options = [dict(label = 'male', value = 'male'),
                                                                         dict(label = 'female', value = 'female')], 
                                                                         value = 'male', style = {'order': '1'}),
                                    dbc.RadioItems(id = 'has-name', options = [dict(label = 'yes', value = 'yes'),
                                                                    dict(label = 'no', value = 'no')], 
                                                                    value = 'yes', style = {'order': '2'}),
                                    dcc.Input(id="intake-age-days", placeholder="Intake age (days)", type="number", value = 40, disabled = False, debounce = True, min=0, max=10000, step=1),
                                    dbc.RadioItems(id = 'sterilized', options = [dict(label = 'yes', value = 'yes'),
                                                                      dict(label = 'no', value = 'no')], 
                                                                      value = 'yes', style = {'order': '3'}),
                                    dcc.Input(id="days-spent", placeholder="Days spent at shelter", type="number", value= 0, disabled = False, debounce = True, min=0, max=10000, step=1, style = {'order': '4'}),
                                    dcc.Input(id="lat", placeholder="Found location (latitude)", type="number", value = 30.266666, disabled = False, debounce = True, min=0, max=10000, step=1, style = {'order': '5'}),
                                    dcc.Input(id="lon", placeholder="Found location (longitude)", type="number", value = -97.733330, disabled = False, debounce = True, min=0, max=10000, step=1, style = {'order': '6'}),

                                    dbc.DropdownMenu(
                                        id = 'breed',
                                        label="Breed",
                                        children=[
                                            dbc.DropdownMenuItem("american shorthair"),
                                            dbc.DropdownMenuItem("domestic longhair"),
                                            dbc.DropdownMenuItem("domestic mediumhair"),
                                            dbc.DropdownMenuItem("domestic shorthair"),
                                            dbc.DropdownMenuItem("other"),
                                            dbc.DropdownMenuItem("siamese")
                                        ],
                                        style = {'order': '7'}
                                    ),
                                    
                                    dbc.DropdownMenu(
                                        id = 'coat-pattern',
                                        label="Coat pattern",
                                        children=[
                                            dbc.DropdownMenuItem("agouti"),
                                            dbc.DropdownMenuItem("brindle"),
                                            dbc.DropdownMenuItem("calico"),
                                            dbc.DropdownMenuItem("point"),
                                            dbc.DropdownMenuItem("smoke"),
                                            dbc.DropdownMenuItem("tabby"),
                                            dbc.DropdownMenuItem("torbie"),
                                            dbc.DropdownMenuItem("tortie"),
                                            dbc.DropdownMenuItem("tricolor")
                                        ],
                                        style = {'order': '8'}
                                    ),
                                    
                                    dbc.DropdownMenu(
                                        id = 'coat',
                                        label="Coat",
                                        children=[
                                            dbc.DropdownMenuItem("black"),
                                            dbc.DropdownMenuItem("blue"),
                                            dbc.DropdownMenuItem("brown"),
                                            dbc.DropdownMenuItem("calico"),
                                            dbc.DropdownMenuItem("cream"),
                                            dbc.DropdownMenuItem("flame"),
                                            dbc.DropdownMenuItem("gray"),
                                            dbc.DropdownMenuItem("lynx"),
                                            dbc.DropdownMenuItem("orange"),
                                            dbc.DropdownMenuItem("other"),
                                            dbc.DropdownMenuItem("seal"),
                                            dbc.DropdownMenuItem("silver"),
                                            dbc.DropdownMenuItem("torbie"),
                                            dbc.DropdownMenuItem("tortie"),
                                            dbc.DropdownMenuItem("white")
                                        ],
                                        style = {'order': '9'}
                                    ),
                                    
                                    dbc.DropdownMenu(
                                        id = 'intake-type',
                                        label="Intake type",
                                        children=[
                                            dbc.DropdownMenuItem("euthanasia request"),
                                            dbc.DropdownMenuItem("owner surrender"),
                                            dbc.DropdownMenuItem("public assist"),
                                            dbc.DropdownMenuItem("stray")
                                        ],
                                        style = {'order': '10'}
                                    ),
                                    
                                    dbc.DropdownMenu(
                                        id = 'intake-condition',
                                        label="Intake condition",
                                        children=[
                                            dbc.DropdownMenuItem("aged"),
                                            dbc.DropdownMenuItem("feral"),
                                            dbc.DropdownMenuItem("injured"),
                                            dbc.DropdownMenuItem("normal"),
                                            dbc.DropdownMenuItem("nursing"),
                                            dbc.DropdownMenuItem("other"),
                                            dbc.DropdownMenuItem("pregnant"),
                                            dbc.DropdownMenuItem("sick")
                                        ],
                                        style = {'order': '11'}
                                    )],

                                style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center','width':'95%' }),
                            
                            html.Div([
                                dbc.Button(
                                            "Predict", id="button", className="me-2", n_clicks=0
                                        ),
                                html.P(id = 'prediction')])])

@callback(Output('prediction', 'children'),
          Input('button', 'n_clicks'),
          Input('sex', 'value'),
          Input('has-name', 'value'),
          Input('intake-age-days', 'value'),
          Input('sterilized', 'value'),
          Input('days-spent', 'value'),
          Input('lat', 'value'),
          Input('lon', 'value'),
          Input('breed', 'value'),
          Input('coat-pattern', 'value'),
          Input('coat', 'value'),
          Input('intake-type', 'value'),
          Input('intake-condition', 'value'))
def get_predictions(n_clicks, sex, has_name, intake_age_days, sterilized_intake, days_spent_at_shelter,
                    lat, lon, breed, coat_pattern, coat, intake_type, intake_condition ):
    if n_clicks > 0:
        url = f"http://127.0.0.1:8000/predict?sex={sex}&coat_pattern={coat_pattern}&has_name={has_name}&breed={breed}&coat={coat}&intake_type={intake_type}&intake_condition={intake_condition}&intake_age_days={intake_age_days}&sterilized_intake={sterilized_intake}&days_spent_at_shelter={days_spent_at_shelter}&lat={lat}&lon={lon}"
        prediction = requests.get(url).json()['prediction']
        if prediction == 1:
            return 'This cat is LIKELY to be adopted!'
        elif prediction == 0:
            return 'This cat is NOT LIKELY to be adopted!'
        else:
            'API error'