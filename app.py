import os

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets
    )

app.title = 'tweetiments'

server = app.server

app.layout = html.Div([
    html.H2(
        'Twitter Sentiment Analysis',
        style={
            'textAlign': 'center'
        }
    )
])

if __name__ == '__main__':
    app.run_server(
        port=8000,
        host='127.0.0.1',
        debug=True
        )
