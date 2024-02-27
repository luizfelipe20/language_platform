from time import sleep
from django.core.management.base import BaseCommand
from word.models import Tags, Terms


class Command(BaseCommand):
    help = "OK"


    def handle(self, *args, **options):         
        Terms.objects.filter(tags__term__contains="https:__www.mairovergara.com").delete()
