import json
import time
from datetime import datetime

import dash
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from smarty_plant.data_model.pipeline_data import OrderData, PipelineData
from smarty_plant.helpers.utils import color_mapping, get_pipeline_data
from smarty_plant.kafka.pipeline_consumer import PipelineConsumer
from smarty_plant.kafka.pipeline_producer import PipelineProducer
from smarty_plant.webgui.config import config
from smarty_plant.webgui.layout import get_layout

TOPIC = "smarty_plant"


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
            [Output("pipe-nbr", "options"), Output("pipe-nbr", "value")],
            [Input("ord-type", "value")],
        )
        def update_pipeline_dropdown(order_type):
            return [
                {"label": i, "value": i} for i in config[order_type]["pipelines"]
            ], config[order_type]["pipelines"][0]

        @self._app.callback(
            Output("histogram", "figure"), [Input("timestamp", "value")]
        )
        def update_histogram_figure(timestamp):
            pipelines_data = {}

            for _, dict in self._message_buffer.items():
                for _, message in dict.items():
                    pipe_number, status = get_pipeline_data(message)
                    pipelines_data[pipe_number] = status

            if not pipelines_data:
                raise dash.exceptions.PreventUpdate

            sunburst_data = [
                {
                    "id": status,
                    "parent": "",
                    "value": list(pipelines_data.values()).count(status),
                }
                for status in set(pipelines_data.values())
            ] + [
                {"id": device, "parent": pipelines_data[device], "value": 1}
                for device in pipelines_data
            ]
            colors = [color_mapping.get(entry["id"], "gray") for entry in sunburst_data]
            trace = go.Sunburst(
                ids=[entry["id"] for entry in sunburst_data],
                labels=[entry["id"] for entry in sunburst_data],
                parents=[entry["parent"] for entry in sunburst_data],
                values=[entry["value"] for entry in sunburst_data],
                hovertemplate="%{label}: %{value} devices",
                marker={"colors": colors},
            )

            layout = go.Layout(
                title="Pipeline Status",
                template="plotly_white",
            )

            return {"data": [trace], "layout": layout}

        @self._app.callback(
            Output("timestamp", "value"), [Input("interval_component", "n_intervals")]
        )
        def update_train_id(n):
            return str(datetime.now().strftime("%H:%M:%S"))

        @self._app.callback(
            Output("pipeline-info", "value"),
            [Input("update", "n_clicks")],
            [
                State("ord-type", "value"),
                State("pipe-nbr", "value"),
                State("ord-nbr", "value"),
                State("pipe-stat", "value"),
            ],
            prevent_initial_call=True,
        )
        def update_pipeline_info(click, ord_type, pipe_nbr, ord_nbr, pipe_stat):
            order_data = OrderData(
                ord_nbr, PipelineData(pipe_nbr, pipe_stat, ord_type)
            ).as_dict()
            self._pipeline_producer.produce(
                TOPIC, json.dumps(order_data), int(time.time())
            )
            return str(order_data)

    def stop(self):
        self._pipeline_consumer.close()
