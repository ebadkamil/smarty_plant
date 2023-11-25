import dash_daq as daq
from dash import dash_table, dcc, html

from smarty_plant.webgui.constants import OrderType, PipelineMode

colors_map = ["jet", "Reds", "Viridis", "gray"]


def get_update_pipeline_tab():
    return html.Div(
        className="control-tab",
        children=[
            html.Br(),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Order Type: ", className="leftbox"),
                            dcc.Dropdown(
                                id="ord-type",
                                options=[
                                    {
                                        "label": order_type.value,
                                        "value": order_type.value,
                                    }
                                    for order_type in OrderType
                                ],
                                value=1,
                                className="rightbox",
                            ),
                            html.Label("Pipeline Number: ", className="leftbox"),
                            dcc.Dropdown(
                                id="pipe-nbr",
                                options=[{"label": i, "value": i} for i in range(100)],
                                value=1,
                                className="rightbox",
                            ),
                            html.Label("Order Number: ", className="leftbox"),
                            dcc.Input(
                                id="ord-nbr",
                                type="number",
                                className="rightbox",
                            ),
                            html.Label("Pipeline Status: ", className="leftbox"),
                            dcc.Dropdown(
                                id="pipe-stat",
                                options=[
                                    {"label": mode.value, "value": mode.value}
                                    for mode in PipelineMode
                                ],
                                value=PipelineMode.STANDING_STILL.value,
                                className="rightbox",
                            ),
                            html.Hr(),
                            html.Button("Update", id="update", n_clicks=0),
                        ],
                        className="pretty_container two-thirds column",
                    ),
                    html.Div(
                        dcc.Textarea(
                            id="pipeline-info",
                            placeholder="Pipeline Information",
                            draggable="false",
                            readOnly=True,
                            disabled=True,
                            style={"width": "100%", "height": 380},
                        ),
                        className="one-third column",
                    ),
                ],
                className="row",
            ),
        ],
    )


def get_overview_tab():
    return html.Div(
        className="control-tab",
        children=[
            html.Br(),
            html.Div(
                [
                    html.Div(
                        dash_table.DataTable(
                            id="device-table",
                            columns=[
                                {"name": "Production Pipeline", "id": "pipe_number"},
                                {"name": "Status", "id": "status"},
                            ],
                            style_table={"overflowX": "auto"},
                        ),
                        className="pretty_container one-third column",
                    ),
                    html.Div(dcc.Graph(id="histogram"), className="two-thirds column"),
                ],
                className="row",
            )
        ],
    )


def get_layout(UPDATE_INT=1.0):
    app_layout = html.Div(
        [
            html.Div(
                [
                    dcc.Interval(
                        id="interval_component",
                        interval=UPDATE_INT * 1000,
                        n_intervals=0,
                    ),
                    # dcc.Interval(
                    #     id="psutil_component", interval=2 * 1000, n_intervals=0
                    # ),
                ],
                style=dict(textAlign="center"),
            ),
            # html.Div(
            #     [
            #         daq.Gauge(
            #             id="virtual_memory",
            #             min=0,
            #             value=0,
            #             size=150,
            #             className="leftbox",
            #             style=dict(textAlign="center"),
            #         ),
            #         daq.Gauge(
            #             id="swap_memory",
            #             min=0,
            #             value=0,
            #             size=150,
            #             className="rightbox",
            #             style=dict(textAlign="center"),
            #         ),
            #     ]
            # ),
            daq.LEDDisplay(
                id="timestamp",
                value="1000",
                color="#FF5E5E",
                style=dict(textAlign="center"),
            ),
            html.Br(),
            html.Div(
                children=[
                    dcc.Tabs(
                        parent_className="custom-tabs",
                        className="custom-tabs-container",
                        id="view-tabs",
                        value="update-pipeline",
                        children=[
                            dcc.Tab(
                                className="custom-tab",
                                selected_className="custom-tab--selected",
                                label="Update Pipeline",
                                value="update-pipeline",
                                children=get_update_pipeline_tab(),
                            ),
                            dcc.Tab(
                                className="custom-tab",
                                selected_className="custom-tab--selected",
                                label="Supervisor Overview",
                                value="overview",
                                children=get_overview_tab(),
                            ),
                        ],
                    )
                ]
            ),
        ]
    )

    return app_layout
