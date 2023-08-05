# -*- coding: utf-8 -*-
"""
kafka module
"""

import json

from kafka import (
    KafkaProducer,
    KafkaConsumer
)


class Producer:
    """
    kafka message producer
    """

    def __init__(self, hosts, topic):
        self._topic = topic
        self._producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                       bootstrap_servers=hosts)

    def write(self, msg, key=None):
        """
        send message
        :param msg:
        :param key:
        :return:
        """
        self._producer.send(self._topic, value=msg, key=key)
        self._producer.flush()

    def __str__(self):
        return f"<{self._producer}> - <{self._topic}>"


class Consumer:
    """
    kafka message consumer
    """

    def __init__(self, hosts, topic, group=None):
        self._topic = topic
        self._consumer = KafkaConsumer(topic,
                                       bootstrap_servers=hosts,
                                       value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                       group_id=group)

    def __iter__(self):
        return self

    def __next__(self):
        return self._consumer.__next__()
