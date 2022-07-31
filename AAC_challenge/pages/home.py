import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[

    html.Div([
        html.Div(
            [
                html.H3(children='Explore data',
                        style={
                            'order': '1',
                            'color': 'black',
                            'text-align': 'center'
                        }),
                html.A(href="/explore",
                       children=[
                           html.Img(alt="Dashboard",
                                    src="assets/explore.png",
                                    className="zoom")
                       ],
                       className="blog-post-1")
            ],
            style={
                'display': 'flex',
                'flex-direction': 'column',
                'align-items': 'center',
                'justify-content': 'center',
                'margin-right': '5vw'
            }),
        html.Div(
            [
                html.H3(children='Make predictions',
                        style={
                            'order': '1',
                            'color': 'black',
                            'text-align': 'center'
                        }),
                html.A(href="/predict",
                       children=[
                           html.Img(alt="Predictions",
                                    src="assets/predict.png",
                                    className='zoom')
                       ],
                       className="blog-post-2")
            ],
            style={
                'display': 'flex',
                'flex-direction': 'column',
                'align-items': 'center',
                'justify-content': 'center',
                'margin-right': '5vw'
            }),
        html.Div(
            [
                html.H3(children='Documentation',
                        style={
                            'order': '1',
                            'color': 'black',
                            'text-align': 'center'
                        }),
                html.A(href="https://jhupiterz.notion.site/AAC-Data-Explorer-Documentation-af73e934772b4058a293e53b0d96728c",
                       target = "_blank",
                       children=[
                           html.Img(alt="Documentation",
                                    src="assets/docs.png",
                                    className='zoom')
                       ],
                       className="blog-post-2")
            ],
            style={
                'display': 'flex',
                'flex-direction': 'column',
                'align-items': 'center',
                'justify-content': 'center',
                'margin-right': '5vw'
            })
    ],
             className="blog-posts")
],
                  style={
                      'display': 'flex',
                      'flex-direction': 'column',
                      'align-items': 'center',
                      'justify-content': 'center',
                      'margin-top': '15vh'
                  })
