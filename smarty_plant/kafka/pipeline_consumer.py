import time
import uuid
from threading import Thread
from typing import Dict, List
import json

from confluent_kafka import Consumer  # type: ignore


class PipelineConsumer:
    def __init__(self, broker: str, topics: List[str]):
        self._broker = broker
        self._topics = topics

        self._stop = False

        self._message_buffer: Dict[str, Dict] = {
            topic: {} for topic in self._topics
        }

        self._consumers = {}
        self._consumer_threads = {}
        try:
            for topic in self._topics:
                conf = {
                    "bootstrap.servers": self._broker,
                    "auto.offset.reset": "latest",
                    "group.id": uuid.uuid4(),
                }
                self._consumers[topic] = Consumer(conf)
                self._consumer_threads[topic] = Thread(
                    target=self._consume, args=(topic,)
                )
        except Exception as error:
            print(f"Unable to create consumers: {error}")
            raise

    @property
    def consumers(self):
        return self._consumers.values()

    @property
    def message_buffer(self):
        return self._message_buffer

    def subscribe(self):
        if not self._topics:
            print("Empty topic list")
            return

        for topic, consumer in self._consumers.items():
            # Remove all the subscribed topics
            consumer.unsubscribe()
            existing_topics = consumer.list_topics().topics

            if topic not in existing_topics:
                print(
                    f"Provided topic {topic} does not exist. \n"
                    f"Available topics are {list(existing_topics.keys())}"
                )
                consumer.close()
                continue

            consumer.subscribe([topic])
            self._consumer_threads[topic].start()

    def _consume(self, topic: str):
        while not self._stop:
            time.sleep(1)
            msg = self._consumers[topic].poll(1)
            if msg is None:
                continue
            if msg.error():
                print(f"Error: {msg.error()}")
            else:
                value = msg.value()
                topic = msg.topic()
                self._update_message_buffer(topic, json.loads(value))

    def _update_message_buffer(self, topic, value):
        self._message_buffer[topic][time.time()] = value

    def close(self):
        self._stop = True
        for _, thread in self._consumer_threads.items():
            if thread and thread.is_alive():
                thread.join()

        for _, consumer in self._consumers.items():
            consumer.close()