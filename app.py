import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

import datetime
import re

from textblob import TextBlob

import nltk
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialise the app
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets
    )

app.title = 'tweetiments'

server = app.server

# Define the app
app.layout = html.Div(
    children=[
    html.H2(
        'Twitter Sentiment Analysis',
        style={
            'textAlign': 'center'
        }
    ),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['#AmericaOrTrump']],
        value='#AmericaOrTrump'
    ),

    html.Div(id='display-value'),
    html.Div(id='update-sentiment'),

    dcc.Interval(
        id='interval-component-slow',
        interval=1*10000, # in milliseconds
        n_intervals=0
    )

    ],
    style={'padding': '20px'}
)

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])

def display_value(value):
    if value is None:
        return 'Select a hashtag'
    return 'Selected hashtag: {}'.format(value)

@app.callback(Output('update-sentiment', 'children'),
              [Input('interval-component-slow', 'n_intervals')])

def update_sentiment_viz(n):

    # Load data
    df_path = os.path.join('data', 'clean_tweets.csv')

    parse_dates = ['date', 'time']
    df = pd.read_csv(
        df_path,
        parse_dates=parse_dates
    )

    pol = lambda x: TextBlob(x).sentiment.polarity
    df['polarity'] = df['tweet'].apply(pol)
    df['polarity'] = df['polarity'].apply(lambda x: 1 if x > 0.1 else -1 if x < -0.1 else 0)

    # Clean and transform data to enable time series
    result = df.groupby(
        [
            pd.Grouper(
                key='time',
                freq='20s'
            ),
            'polarity'
        ]
    ).count().unstack(fill_value=0).stack().reset_index()

    time_series = result['time'][result['polarity']==0].reset_index(drop=True)

    # Create the graph 
    children = [
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='crossfilter-indicator-scatter',
                            figure={
                                'data': [
                                    go.Scatter(
                                        x=time_series,
                                        y=result['id'][result['polarity']==0].reset_index(drop=True),
                                        name="Neutral",
                                        opacity=0.8,
                                        mode='lines',
                                        line=dict(width=0.5, color='rgb(141, 147, 249)'),
                                        stackgroup='one' 
                                    ),
                                    go.Scatter(
                                        x=time_series,
                                        y=result['id'][result['polarity']==-1].reset_index(drop=True),
                                        name="Negative",
                                        opacity=0.8,
                                        mode='lines',
                                        line=dict(width=0.5, color='rgb(244, 66, 66)'),
                                        stackgroup='two' 
                                    ),
                                    go.Scatter(
                                        x=time_series,
                                        y=result['id'][result['polarity']==1].reset_index(drop=True),
                                        name="Positive",
                                        opacity=0.8,
                                        mode='lines',
                                        line=dict(width=0.5, color='rgb(66, 245, 81)'),
                                        stackgroup='three' 
                                    )
                                ]
                            }
                        )
                    ],
                    style={'width': '73%', 'display': 'inline-block', 'padding': '0 0 0 20'}),

                    ],

                    style={'marginLeft': 70}
                )
            ]
    return children

# Run the app
if __name__ == '__main__':
    app.run_server(
        port=8000,
        host='127.0.0.1',
        debug=True
    )
