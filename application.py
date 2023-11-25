# from smarty_plant.kafka.pipeline_producer import PipelineProducer
# import json
# import time

# producer = PipelineProducer("localhost:9093")

# topic, message = "test_2", "hello world"
# producer.produce(topic, json.dumps(message), int(time.time()))
# producer.close()

from smarty_plant.webgui.app import DashApp



app = DashApp()

app._app.run_server(debug=False)
