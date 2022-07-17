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

                            html.H3('Parameters', style = {'order':'1', 'text-align': 'left', 'margin-bottom': '3vh'}),

                            html.Div([

                                html.Div([ 
                                    html.Label('Sex', style={'font-weight': 'bold'}),
                                    dbc.RadioItems(id = 'sex', options = [dict(label = 'male', value = 'male'),
                                                                         dict(label = 'female', value = 'female')], 
                                                                        style = {'order': '1', 'margin-right': '2vw'})]),
                                
                                html.Div([
                                    html.Label('Has a name', style={'font-weight': 'bold'}),
                                    dbc.RadioItems(id = 'has-name', options = [dict(label = 'yes', value = 'yes'),
                                                                    dict(label = 'no', value = 'no')], 
                                                                    style = {'order': '2', 'margin-right': '2vw', 'width': '8vw'})]),
                                
                                html.Div([
                                    html.Label('Intake age (days)', style={'font-weight': 'bold'}),
                                    dcc.Input(id="intake-age-days", placeholder="Intake age (days)", value=0, type="number", disabled = False, debounce = True, min=0, max=10000, step=1, style = {'order': '3', 'width': '8vw', 'margin-right': '2vw'})]),

                                html.Div([
                                    html.Label('Sterilized', style={'font-weight': 'bold'}),
                                    dbc.RadioItems(id = 'sterilized', options = [dict(label = 'yes', value = 'yes'),
                                                                      dict(label = 'no', value = 'no')], 
                                                                      style = {'order': '4', 'margin-right': '4vw'})]),
                                
                                html.Div([
                                    html.Label('Days spent at shelter', style={'font-weight': 'bold'}),
                                    dcc.Input(id="days-spent", placeholder="Days spent at shelter", value=0, type="number", disabled = False, debounce = True, min=0, max=10000, step=1, style = {'order': '5', 'width': '11vw', 'margin-right': '2vw'})]),
                                    
                                html.Div([  
                                    html.Label('Found location (latitude)', style={'font-weight': 'bold'}),  
                                    dcc.Input(id="lat", placeholder="Found location (latitude)", value=0, type="number", min = -360, max = 360, disabled = False, debounce = True, step=0.000001, style = {'order': '6', 'width': '14vw', 'margin-right': '2vw'})]),
                                    
                                html.Div([   
                                    html.Label('Found location (longitude)', style={'font-weight': 'bold'}), 
                                    dcc.Input(id="lon", placeholder="Found location (longitude)", value=0, type="number", min = -360, max = 360, disabled = False, debounce = True, step=0.000001, style = {'order': '7', 'width': '14vw', 'margin-right': '2vw'})])],
                                    style = {'order':'2', 'display': 'flex', 'flex-direction': 'row', 'width': '95vw', 'height': '4vh', 'margin':'auto', 'margin-bottom': '6vh'}),
                            
                            html.Div([

                                html.Div([
                                    html.Label('Breed', style={'font-weight': 'bold'}),
                                    dcc.Dropdown(
                                        id = 'breed',
                                        clearable = False,
                                        placeholder="Breed",
                                        value = 'domestic shorthair',
                                        options=[
                                            "american shorthair",
                                            "domestic longhair",
                                            "domestic mediumhair",
                                            "domestic shorthair",
                                            "other",
                                            "siamese"
                                        ],
                                        style = {'order': '1', 'width': '11vw', 'margin-right': '2vw'}
                                    )]),

                                html.Div([
                                    html.Label('Coat pattern', style={'font-weight': 'bold'}),
                                    dcc.Dropdown(
                                        id = 'coat-pattern',
                                        placeholder="Coat pattern",
                                        clearable = False,
                                        value = 'agouti',
                                        options=[
                                            "agouti",
                                            "brindle",
                                            "calico",
                                            "point",
                                            "smoke",
                                            "tabby",
                                            "torbie",
                                            "tortie",
                                            "tricolor"
                                        ],
                                        style = {'order': '2', 'width': '9vw', 'margin-right': '2vw'}
                                    )]),

                                html.Div([
                                    html.Label('Coat', style={'font-weight': 'bold'}),
                                    dcc.Dropdown(
                                        id = 'coat',
                                        placeholder="Coat",
                                        clearable = False,
                                        value = 'black',
                                        options=[
                                            "black",
                                            "blue",
                                            "brown",
                                            "calico",
                                            "cream",
                                            "flame",
                                            "gray",
                                            "lynx",
                                            "orange",
                                            "other",
                                            "seal",
                                            "silver",
                                            "torbie",
                                            "tortie",
                                            "white"
                                        ],
                                        style = {'order': '3', 'width': '5vw', 'margin-right': '2vw'}
                                    )]),
                                    
                                html.Div([
                                    html.Label('Intake type', style={'font-weight': 'bold'}),
                                    dcc.Dropdown(
                                        id = 'intake-type',
                                        placeholder="Intake type",
                                        clearable = False,
                                        value = 'stray',
                                        options=[
                                            "euthanasia request",
                                            "owner surrender",
                                            "public assist",
                                            "stray"
                                        ],
                                        style = {'order': '4', 'width': '10vw', 'margin-right': '2vw'}
                                    )]),
                                    
                                html.Div([
                                    html.Label('Intake condition', style={'font-weight': 'bold'}),
                                    dcc.Dropdown(
                                        id = 'intake-condition',
                                        clearable = False,
                                        placeholder="Intake condition",
                                        value = 'normal',
                                        options=[
                                            "aged",
                                            "feral",
                                            "injured",
                                            "normal",
                                            "nursing",
                                            "other",
                                            "pregnant",
                                            "sick"
                                        ],
                                        style = {'order': '5', 'width': '9vw', 'margin-right': '2vw'}
                                    )])], style = {'order':'3', 'display': 'flex', 'flex-direction': 'row', 'width': '95vw', 'margin':'auto', 'margin-bottom': '3vh'}),
                                    
                                    dbc.Button(
                                            "Predict", id="button", className="me-2", n_clicks=0, style = {'order': '4'}
                                        ),
                                
                                html.H3(id = 'prediction', style = {'order': '5', 'margin-top': '4vh'})],

                                style = {'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'width':'95%', 'margin': 'auto'}),
                            
                            ])

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
        results = requests.get(url).json()
        prediction = results['prediction']
        #proba_0 = results['prob_0']
        proba_1 = results['prob_1']
        if prediction == 1:
            return f'This cat is LIKELY to be adopted! ({round(proba_1, 2)*100}%)'
        elif prediction == 0:
            return f'This cat is NOT LIKELY to be adopted! ({round(proba_1, 2)*100}%)'
        else:
            'API error'