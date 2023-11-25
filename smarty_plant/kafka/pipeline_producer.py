import json
import time

from confluent_kafka import Producer

from smarty_plant.helpers.utils import run_in_thread


class PipelineProducer:
    def __init__(self, broker: str):
        self._broker = broker
        self._producer = Producer({"bootstrap.servers": self._broker})
        self._stop = False
        self._poller_t = self._start_polling_producer()

    @run_in_thread
    def _start_polling_producer(self):
        while not self._stop:
            self._producer.poll(0.5)

    def close(self):
        self._stop = True
        self._poller_t.join()
        self._producer.flush(2)

    def produce(self, topic: str, payload: bytes, timestamp: int):
        def ack(err, _):
            if err:
                print(f"Message failed delivery: {err} \n")

        try:
            self._producer.produce(topic, payload, on_delivery=ack, timestamp=timestamp)
        except Exception as error:
            print(f"Message failed delivery: {error} \n")
        self._producer.poll(0)
