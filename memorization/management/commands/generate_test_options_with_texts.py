
from word.models import ShortText
from memorization.models import ShortTextMemorizationTest
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "OK"

    def add_arguments(self, parser):
        ...

    def handle(self, *args, **options): 
        for elem in ShortText.objects.exclude(audio=None):
            ShortTextMemorizationTest.objects.create(**{
                "scrambled_text": elem.scrambled_text, 
                "reference": ShortText.objects.get(id=elem.id),
                "audio": elem.audio
            })
