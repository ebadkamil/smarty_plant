
from smarty_plant.webgui.app import DashApp


app = DashApp()

try:
    app._app.run_server(debug=False)
except KeyboardInterrupt:
    print(f"Interrupted by user: Closing consumers ...")
finally:
    app.stop()

# from dash import dash_table, dcc, html
# import random

# import dash
# from dash.dependencies import Input, Output
# import random
# import plotly.graph_objs as go

# # Sample data for 100 devices
# devices = [f"Device {i}" for i in range(1, 3)]
# device_states = {device: random.choice(["Red", "Green", "Yellow"]) for device in devices}

# # Create Dash app
# app = dash.Dash(__name__)

# # Layout of the app
# app.layout = html.Div([
#     html.H1("Device Status Sunburst"),
#     dcc.Graph(id='device-status-sunburst'),
#     dcc.Interval(
#         id='interval-component',
#         interval=10*1000,  # in milliseconds, updates every 10 seconds
#         n_intervals=0
#     ),
# ])

# # Callback to update the sunburst plot
# @app.callback(
#     Output('device-status-sunburst', 'figure'),
#     [Input('interval-component', 'n_intervals')]
# )
# def update_sunburst(n_intervals):
#     # Update device states
#     for device in device_states:
#         device_states[device] = random.choice(["Red", "Green", "Yellow"])

#     # Create a list of dictionaries for sunburst data
#     sunburst_data = [
#         {"id": status, "parent": "", "value": list(device_states.values()).count(status)} for status in set(device_states.values())
#     ] + [
#         {"id": device, "parent": device_states[device], "value": 1} for device in device_states
#     ]

#     # Assign specific colors to each status category
#     status_colors = {"Red": "red", "Green": "green", "Yellow": "yellow"}
#     colors = [status_colors.get(entry["id"], "gray") for entry in sunburst_data]
#     print(colors)
#     print(sunburst_data)
#     # Create a Plotly figure using go.Sunburst
#     trace = go.Sunburst(
#         ids=[entry["id"] for entry in sunburst_data],
#         labels=[entry["id"] for entry in sunburst_data],
#         parents=[entry["parent"] for entry in sunburst_data],
#         values=[entry["value"] for entry in sunburst_data],
#         hovertemplate='%{label}: %{value} devices',
#         marker=dict(
#             colors=colors,
#             line=dict(width=0.5, color='black'),  # Add border line
#         ),
#     )

#     layout = dict(
#         title='Device Status Sunburst',
#         template='plotly_white',  # White background theme
#     )

#     return {'data': [trace], 'layout': layout}

# if __name__ == '__main__':
#     app.run_server(debug=True)