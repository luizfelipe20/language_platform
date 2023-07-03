import os
from django.core.management.base import BaseCommand

from memorization.consumers.verbs_conjugation_consumer import pull_queue, setup_broker


class Command(BaseCommand):
    help = "OK"

    # def add_arguments(self, parser):
    #     parser.add_argument("", nargs="+", type=int)

    def handle(self, *args, **options):      
        queue_name = "fila_2"
        exchange_name = "exchange_2"
        rabbitmq_instance = setup_broker(queue_name, exchange_name)

        pull_queue(rabbitmq_instance)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully !!!')
        )