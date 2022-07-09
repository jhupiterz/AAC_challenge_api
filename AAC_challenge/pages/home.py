import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='Welcome to Austin Animal Center Data Explorer', style = {'order':'1', 'color': 'black'}),

    html.Div([
            
            html.Div([
                html.H3(children = 'Explore data', style = {'order': '1','color': 'black', 'text-align': 'center'}),
                html.A(
                        href="/explore",
                        children=[
                            html.Img(
                                alt="Dashboard",
                                src="assets/dashboard.png",
                                className="zoom"
                            )
                        ], className= "blog-post-1"
                    )], style = {'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center', 'margin-right': '5vw'}),
                
            html.Div([
                html.H3(children = 'Make predictions', style = {'order': '1','color': 'black', 'text-align': 'center'}),
                html.A(
                        href="/predict",
                        children=[
                            html.Img(
                                alt="Predictions",
                                src="assets/predict.png",
                                className='zoom'
                            )
                        ], className= "blog-post-2"
                    )], style = {'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center', 'margin-right': '5vw'})
                        ],className= "blog-posts")

], style = {'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center', 'margin-top': '15vh'})