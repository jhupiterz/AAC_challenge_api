import pandas as pd
from AAC_challenge import utils

import plotly.express as px

def get_outcome_age_histogram(df, adoptions_only=False):
    if adoptions_only==True:
        df = df[df['outcome_type'] == 'Adoption']
        title = 'Adoptions only'
    else:
        title = 'All outcomes'
    fig = px.histogram(df, x='outcome_age_(years)', nbins= 30, color = 'sex', title = title)
    return fig

def get_outcome_sterilized_histogram(df):
    fig = px.histogram(df, x='outcome_type', color = 'sex', pattern_shape="sterilized_outcome")
    return fig

def get_outcome_weekday_histogram(df):
    fig = px.histogram(df, x='outcome_weekday', color = 'outcome_type')
    return fig

def get_has_name_histogram(df):
    fig = px.histogram(df, x = 'outcome_type', color = 'has_name')
    return fig

def get_outcome_timeseries(df):
    outcome_date = df.groupby(['outcome_year_month', 'outcome_type'], as_index=False).count()[['outcome_year_month', 'outcome_type', 'sex']]
    outcome_date['outcome_year_month'] = pd.to_datetime(outcome_date['outcome_year_month'])
    outcome_date = outcome_date.sort_values('outcome_year_month', ascending=True)
    fig = px.line(outcome_date, x = 'outcome_year_month', y = 'sex', color = 'outcome_type')
    fig.update_yaxes(title = 'number of outcomes')
    fig.update_xaxes()
    return fig

def get_top_breeds_pie(df, adoptions_only = False):
    if adoptions_only==True:
        df = df[df['outcome_type'] == 'Adoption']
        title = 'Adoptions only'
    else:
        title = 'All outcomes'
    #df['top_breeds'] = df.breed.apply(utils.map_top_breeds)
    fig = px.pie(df.groupby('top_breeds', as_index=False).count().sort_values('sex', ascending=False), values='sex', names='top_breeds', title=title)
    return fig
