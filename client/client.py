"""
This module is the topmost layer which will interact with clients,
Its will take input, create a message in KfMessage format,
and send the request through kafka on "kf.vector.ai.requests"
and consume response on "kf.vector.ai.responses.{client_id}"

"""
from middleware.kafkaconsumerproducer import KafkaConsumerProducer

import json
import uuid


class Client(object):
    def __init__(self, config):
        self._config = config
        self._queue = KafkaConsumerProducer(config["kafka"], self.process_message)
        self._id = uuid.uuid4()
        self._queue.start(topic_suffix=f".{self._id}")

    def process_message(self, msg):
        print("Received response {msg}")

    def insert_continent(self, name, population, area):
        kfmsg = {
            "request_id": uuid.uuid4(),
            "type": "INSERT_CONTINENT",
            "client_id": self._id,
            "values": {"name": name, "population": population, "area": area},
        }

        self._send_request(kfmsg)

    def insert_country(
        self,
        name,
        population,
        area,
        num_hospitals,
        num_rivers,
        num_schools,
        parent_continent,
    ):
        kfmsg = {
            "request_id": uuid.uuid4(),
            "type": "INSERT_COUNTRY",
            "client_id": self._id,
            "values": {
                "name": name,
                "population": population,
                "area": area,
                "num_hospitals": num_hospitals,
                "num_rivers": num_rivers,
                "num_schools": num_schools,
                "parent_continent": parent_continent,
            },
        }

        self._send_request(kfmsg)

    def insert_city(
        self,
        name,
        population,
        area,
        num_roads,
        num_trees,
        num_shops,
        num_schools,
        parent_country,
    ):
        kfmsg = {
            "request_id": uuid.uuid4(),
            "type": "INSERT_CITY",
            "client_id": self._id,
            "values": {
                "name": name,
                "population": population,
                "area": area,
                "num_roads": num_roads,
                "num_trees": num_trees,
                "num_shops": num_shops,
                "num_schools": num_schools,
                "parent_country": parent_country,
            },
        }

        self._send_request(kfmsg)

    def _send_request(self, msg):
        self._queue.send(json.dumps(msg), self._config["producer"]["topic_prefix"])
