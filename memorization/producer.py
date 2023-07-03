import json
import os
import logging
import pika
from enum import Enum


class RabbitMQ():

    def __init__(self, queue, host, routing_key, username, password, exchange=''):
        self._queue = queue
        self._host = host
        self._routing_key = routing_key
        self._exchange = exchange
        self._username = username
        self._password = password
        self.start_server()

    def start_server(self):
        self.create_channel()
        self.create_exchange()
        self.create_bind()
        logging.info("Channel created...")

    def create_channel(self):
        credentials = pika.PlainCredentials(username=self._username, password=self._password)
        parameters = pika.ConnectionParameters(self._host, credentials=credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

    def create_exchange(self):
        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type='direct',
            passive=False,
            durable=True,
            auto_delete=False
        )
        self._channel.queue_declare(queue=self._queue, durable=False)

    def create_bind(self):
        self._channel.queue_bind(
            queue=self._queue,
            exchange=self._exchange,
            routing_key=self._routing_key
        )

    def publish(self, message={}):
        """
        :param message: message to be publish in JSON format
        """

        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=self._routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(content_type='application/json')
        )
        logging.info("Published Message: {}".format(message))


def setup_broker(queue_name, exchange_name):
    rabbitmq_instance = RabbitMQ(
        queue=queue_name,
        host=os.environ.get("RABBITMQ_HOST"),
        routing_key=os.environ.get("RABBITMQ_ROUTING_KEY"),
        username=os.environ.get("RABBITMQ_USERNAME"),
        password=os.environ.get("RABBITMQ_PASSSWORD"),
        exchange=exchange_name
    )
    return rabbitmq_instance


def push_queue(instance:RabbitMQ, payload:dict):
    instance.publish(message=payload)