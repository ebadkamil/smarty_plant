import time
from datetime import datetime

import json
import dash
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from smarty_plant.webgui.layout import get_layout
from smarty_plant.kafka.pipeline_producer import PipelineProducer
from smarty_plant.data_model.pipeline_data import PipelineData, OrderData
from smarty_plant.kafka.pipeline_consumer import PipelineConsumer
from smarty_plant.helpers.utils import get_pipeline_data, color_mapping


TOPIC="smarty_plant"


class DashApp:
    def __init__(self):
        app = dash.Dash(__name__)
        app.config["suppress_callback_exceptions"] = True
        self._app = app
        self._data_client = None
        self._pipeline_producer = PipelineProducer("localhost:9093")

        self._pipeline_consumer = PipelineConsumer("localhost:9093", [TOPIC])
        self._message_buffer = self._pipeline_consumer.message_buffer
        self._pipeline_consumer.subscribe()

        self.setLayout()
        self.register_callbacks()

    def setLayout(self):
        self._app.layout = get_layout()

    def register_callbacks(self):
        @self._app.callback(
            Output("histogram", "figure"), [Input("timestamp", "value")]
        )
        def update_histogram_figure(timestamp):
            pipelines_data = {}

            for topic, dict in self._message_buffer.items():
                for key, message in dict.items():
                    pipe_number, status = get_pipeline_data(message)
                    pipelines_data[pipe_number] = status

            if not pipelines_data:
                raise dash.exceptions.PreventUpdate

            traces = [
                go.Bar(
                    x=list(pipelines_data.keys()),
                    y=[1] * len(pipelines_data),
                    marker_color=[color_mapping[status] for status in pipelines_data.values()],
                    text=list(pipelines_data.values()),
                    hoverinfo="text+x+name",
                )
            ]
            figure = {
                "data": traces,
                "layout": go.Layout(
                    margin={"l": 40, "b": 40, "t": 40, "r": 10},
                    xaxis={"title": "State"},
                    yaxis={"title": f"Number of Pipelines"},
                ),
            }

            return figure

        @self._app.callback(
            Output("timestamp", "value"), [Input("interval_component", "n_intervals")]
        )
        def update_train_id(n):
            return str(datetime.now().strftime("%H:%M:%S"))

        @self._app.callback(
            Output("pipeline-info", "value"),
            [Input('update', 'n_clicks')],
            [State("ord-type", "value"),
             State("pipe-nbr", "value"),
             State("ord-nbr", "value"),
             State("pipe-stat", "value"),
            ],
            prevent_initial_call=True
        )
        def update_pipeline_info(click, ord_type, pipe_nbr, ord_nbr, pipe_stat):
            order_data = OrderData(
                ord_nbr,
                PipelineData(
                    pipe_nbr, pipe_stat, ord_type
                )
            ).as_dict()
            self._pipeline_producer.produce(TOPIC, json.dumps(order_data), int(time.time()))
            return str(order_data)

    def stop(self):
        self._pipeline_consumer.close()