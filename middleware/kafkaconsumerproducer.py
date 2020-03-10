"""
This class would be a wrapper around Kafka library 
taking config as an input to specify producer/consumer topics
It should be able publish to a topic and read from another one
"""

from confluent_kafka import Consumer, Producer, KafkaException

from misc.logger import get_logger

LOG = get_logger()

class KafkaConsumerProducer(object):
    def __ini__(self, config, callback, consumer_id=None):
        self._config = config
        self._consumer = Consumer(self._config["consumer"]["config"])
        self._producer = Producer(self._config["producer"]["config"])
        self._running = False
        self._callback = callback

    def __del__(self):
        LOG.info("Closing consumer")
        self.close()
        LOG.info("Flushing producer")
        self._producer.flush()

    def start(self, topic_suffix=""):
        self._running = True
        try:
            self._consumer.subscribe(
                [self._consumer["consumer"]["topic_prefix"] + topic_suffix]
            )
            while self._running:
                msg = self._consumer.poll(timeout=1.0)
                if msg is None:
                    continue

                if msg.error():
                    raise KafkaException(msg.error())

                LOG.info(f"Received message {msg} from kafka.")

                self._callback(msg)

        except KafkaException as kferror:
            LOG.error(f"LOG: Error fetching messages{str(kferror.error())}")
        finally:
            self.close()

    def close(self):
        self._running = False
        self._consumer.close()

    def send(self, message, topic=None, key=None, suffix=""):

        topic = topic or (self._config["producer"]["topic_prefix"] + suffix)

        def acked(err, msg):
            if err is not None:
                LOG.error(f"Failed to write to kafka {str(msg)} due to {str(err)}")
            else:
                LOG.info(f"Message {msg} produced")

        self._producer.produce(topic, key=key, value=message, callback=acked)
        self._producer.poll(1)
