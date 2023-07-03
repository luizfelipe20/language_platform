import json
import os
import logging
from time import sleep
import pika
from word.crowlers.google_translate import get_sentences, get_translations

from word.models import Tags, Terms, Translation, TypePartSpeechChoices


class RabbitMQConsumer():
    """
    Producer component that will publish message and handle
    connection and channel interactions with RabbitMQ.
    """

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
        self._channel.basic_qos(prefetch_count=1)

    @staticmethod
    def callback(channel, method, properties, body):
        payload = json.loads(body.decode())

        term_instance, _ = Terms.objects.get_or_create(**{"text": payload["term"]})
        tag_instance, _ = Tags.objects.get_or_create(**{"term": payload["tag"]})
        term_instance.tags.add(tag_instance)

        for sentence in get_sentences(term_instance.text):
            Terms.objects.get_or_create(**{"text": sentence, "reference": term_instance})

        translations = get_translations(term_instance.text)
        print(f"translations: {translations}")
        for translation in translations:
            if not len(translations[translation]):
                continue
            Translation.objects.get_or_create(**{"term": translation, "reference": term_instance})

        channel.basic_ack(delivery_tag=method.delivery_tag)

    def get_messages(self):
        try:
            logging.info("Starting the server...")
            self._channel.basic_consume(
                queue=self._queue,
                on_message_callback=RabbitMQConsumer.callback,
            )
            self._channel.start_consuming()            
        except Exception as e:
            logging.debug(f'Exception: {e}')


def setup_broker(queue_name, exchange_name):
    instance_consumer = RabbitMQConsumer(
            queue=queue_name,
            host=os.environ.get("RABBITMQ_HOST"),
            routing_key=os.environ.get("RABBITMQ_ROUTING_KEY"),
            username=os.environ.get("RABBITMQ_USERNAME"),
            password=os.environ.get("RABBITMQ_PASSSWORD"),
            exchange=exchange_name
        )
    return instance_consumer


def pull_queue(instance:RabbitMQConsumer):    
    return instance.get_messages()
