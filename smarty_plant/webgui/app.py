import time
from math import ceil

import dash
import plotly.graph_objs as go
import psutil as ps
from dash.dependencies import Input, Output, State

from smarty_plant.webgui.layout import get_layout


def get_virtual_memory():
    virtual_memory, swap_memory = ps.virtual_memory(), ps.swap_memory()
    return virtual_memory, swap_memory


class DashApp:
    def __init__(self):
        app = dash.Dash(__name__)
        app.config["suppress_callback_exceptions"] = True
        self._app = app
        self._data_client = None
        self.setLayout()
        self.register_callbacks()

    def setLayout(self):
        self._app.layout = get_layout()

    def register_callbacks(self):
        @self._app.callback(
            Output("timestamp", "value"), [Input("interval_component", "n_intervals")]
        )
        def update_train_id(n):
            return str(time.time())
