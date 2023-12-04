
from smarty_plant.webgui.app import DashApp


app = DashApp()

try:
    app._app.run_server(debug=False)
except KeyboardInterrupt:
    print(f"Interrupted by user: Closing consumers ...")
finally:
    app.stop()
