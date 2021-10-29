import json
import dash
import plotly.express as px

from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from websocket import create_connection


app = dash.Dash(__name__)


TELEM = ['light', 'humidity']


class PlantDash:
    def __init__(self, app):
        self.app = app
        self.ws = create_connection(f'ws://127.0.0.1:5000/data')
        self.initial = {k: [0.0] * 200 for k in TELEM}

        elements = []
        for k in TELEM:
            elements.append(html.Div(f'{k} Measurement'))
            elements.append(dcc.Graph(id=f'{k}_graph'))
            elements.append(dcc.Interval(
                id=f'{k}_interval_component',
                interval=1*1000,  # in milliseconds
                n_intervals=0
            ))
        self.app.layout = html.Div(elements)

        @self.app.callback(
            Output('light_graph', 'figure'),
            Input('light_interval_component', 'n_intervals')
        )
        def update_light(n_intervals):
            telem = json.loads(self.ws.recv())

            data = self.initial['light']
            data.append(telem['light'])
            data.pop(0)

            figure = px.line(
                {
                    'Time': [i for i in range(len(data))],
                    'light': data
                },
                x='Time',
                y='light',
                range_y=[0, 1]
            )

            return figure

        @self.app.callback(
            Output('humidity_graph', 'figure'),
            Input('humidity_interval_component', 'n_intervals')
        )
        def update_humidity(n_intervals):
            telem = json.loads(self.ws.recv())

            data = self.initial['humidity']
            data.append(telem['humidity'])
            data.pop(0)

            figure = px.line(
                {
                    'Time': [i for i in range(len(data))],
                    'humidity': data
                },
                x='Time',
                y='humidity',
                range_y=[0, 1]
            )

            return figure


if __name__ == '__main__':
    PlantDash(app)
    app.run_server(host='0.0.0.0', port=80)  # , debug=True)
